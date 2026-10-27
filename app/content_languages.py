"""Bounded metadata-only RSS requests with public-IP pinning and persistent cache."""
import http.client
import ipaddress
import json
import re
import socket
import sqlite3
import ssl
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from defusedxml import ElementTree

LANGUAGES = {'tr': 'Türkçe', 'en': 'İngilizce', 'de': 'Almanca', 'fr': 'Fransızca',
             'es': 'İspanyolca', 'it': 'İtalyanca', 'pt': 'Portekizce', 'ar': 'Arapça',
             'ru': 'Rusça', 'ja': 'Japonca', 'ko': 'Korece', 'zh': 'Çince', 'nl': 'Felemenkçe'}
ALIASES = {'turkish': 'tr', 'türkçe': 'tr', 'tur': 'tr', 'english': 'en', 'eng': 'en',
           'german': 'de', 'deu': 'de', 'ger': 'de', 'french': 'fr', 'fra': 'fr',
           'spanish': 'es', 'spa': 'es', 'italian': 'it', 'ita': 'it', 'portuguese': 'pt',
           'arabic': 'ar', 'russian': 'ru', 'japanese': 'ja', 'korean': 'ko', 'chinese': 'zh', 'dutch': 'nl'}


def normalize_language(value):
    if not isinstance(value, str):
        return None
    value = value.strip().lower().replace('_', '-')
    value = ALIASES.get(value, value.split('-')[0])
    return value if value in LANGUAGES else None


def public_target(url):
    p = urlsplit(url)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('Invalid feed URL')
    port = p.port or (443 if p.scheme == 'https' else 80)
    if port != (443 if p.scheme == 'https' else 80):
        raise ValueError('Non-standard feed port')
    addresses = list(dict.fromkeys(info[4][0] for info in socket.getaddrinfo(p.hostname, port, type=socket.SOCK_STREAM)))
    if not addresses or any(not ipaddress.ip_address(ip).is_global for ip in addresses):
        raise ValueError('Non-public feed destination')
    return p, port, addresses[0]


class FoundLanguage(Exception):
    def __init__(self, language):
        self.language = language


class LanguageTarget:
    def __init__(self):
        self.path, self.text = [], ''

    def start(self, tag, attributes):
        self.path.append(tag)
        if self.path == ['rss', 'channel', 'language']:
            self.text = ''

    def data(self, data):
        if self.path == ['rss', 'channel', 'language']:
            self.text += data

    def end(self, tag):
        if self.path == ['rss', 'channel', 'language']:
            raise FoundLanguage(normalize_language(self.text))
        self.path.pop()

    def close(self):
        return None


def read_public(url, max_bytes=1024 * 1024, rss=False):
    """Revalidate redirects; socket uses the vetted IP while TLS verifies the real hostname."""
    deadline = time.monotonic() + 12
    for _ in range(4):
        p, port, ip = public_target(url)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('Metadata deadline')
        cls = http.client.HTTPSConnection if p.scheme == 'https' else http.client.HTTPConnection
        conn = cls(p.hostname, port, timeout=min(5, remaining))
        conn._create_connection = lambda address, timeout, source_address=None: socket.create_connection(
            (ip, port), timeout, source_address)
        try:
            path = p.path or '/'
            if p.query:
                path += '?' + p.query
            conn.request('GET', path, headers={'User-Agent': 'TasteTrip/0.1 (podcast language metadata)',
                                               'Accept-Encoding': 'identity'})
            response = conn.getresponse()
            if response.status in (301, 302, 303, 307, 308):
                target = urljoin(url, response.getheader('Location', ''))
                if urlsplit(url).scheme == 'https' and urlsplit(target).scheme != 'https':
                    raise ValueError('HTTPS downgrade')
                url = target
                continue
            if response.status != 200 or response.getheader('Content-Encoding', 'identity') != 'identity':
                raise ValueError('Metadata unavailable')
            size = response.getheader('Content-Length')
            if size and int(size) > max_bytes and not rss:
                raise ValueError('Metadata too large')
            chunks, total = [], 0
            parser = ElementTree.DefusedXMLParser(target=LanguageTarget(), forbid_dtd=True) if rss else None
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError('Metadata deadline')
                if conn.sock:
                    conn.sock.settimeout(min(3, remaining))
                chunk = response.read1(min(16384, max_bytes + 1 - total))
                if not chunk:
                    return parser.close() if rss else b''.join(chunks)
                if parser:
                    try:
                        parser.feed(chunk)
                    except FoundLanguage as found:
                        return found.language
                else:
                    chunks.append(chunk)
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError('Metadata too large')
        finally:
            conn.close()
    raise ValueError('Too many redirects')


def rss_language(xml_bytes):
    root = ElementTree.fromstring(xml_bytes)
    return normalize_language(root.findtext('./channel/language'))


def lookup_podcast_language(itunes_id, cache_dir):
    if not re.fullmatch(r'[0-9]{1,20}', str(itunes_id)):
        return {'language': None, 'language_source': None}
    path = Path(cache_dir) / 'content-language-cache.sqlite3'
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path, timeout=15)) as db:
        db.execute('CREATE TABLE IF NOT EXISTS cache(id TEXT PRIMARY KEY, body TEXT, expires REAL)')
        row = db.execute('SELECT body FROM cache WHERE id=? AND expires>?', (str(itunes_id), time.time())).fetchone()
        if row:
            cached = json.loads(row[0])
            if 'apple_url' in cached:
                return cached
    result = {'language': None, 'language_source': None, 'apple_url': None}
    try:
        data = json.loads(read_public('https://itunes.apple.com/lookup?id=' + str(itunes_id) + '&entity=podcast'))
        item = next((r for r in data.get('results', []) if str(r.get('collectionId')) == str(itunes_id)), None)
        if item:
            apple = item.get('collectionViewUrl') or item.get('trackViewUrl') or ''
            parsed = urlsplit(apple)
            if parsed.scheme == 'https' and parsed.hostname == 'podcasts.apple.com' and not parsed.username and not parsed.password:
                result['apple_url'] = apple
            language = read_public(item['feedUrl'], rss=True) if item.get('feedUrl') else None
            if language:
                result.update(language=language, language_source='RSS · yayıncı beyanı',
                              language_checked_at=int(time.time()))
    except (OSError, ValueError, http.client.HTTPException, ElementTree.ParseError):
        pass
    except Exception as error:
        # defusedxml rejects DTD/entities with its own exception hierarchy.
        from defusedxml.common import DefusedXmlException
        if not isinstance(error, DefusedXmlException):
            raise
    with closing(sqlite3.connect(path, timeout=15)) as db:
        db.execute('INSERT OR REPLACE INTO cache VALUES (?,?,?)',
                   (str(itunes_id), json.dumps(result), time.time() + (7 * 86400 if result['language'] else 3600)))
        db.commit()
    return result


def enrich_podcast_links(items, cache_dir):
    with ThreadPoolExecutor(max_workers=4) as executor:
        metadata = list(executor.map(lambda item: lookup_podcast_language(item.get('itunes_id'), cache_dir), items))
    return [{**item, **meta} for item, meta in zip(items, metadata)]


def filter_content_language(items, kind, language, cache_dir):
    if language == 'any':
        return items[:4], {'requested': 'any', 'checked': 0, 'unknown': 0, 'matched': len(items[:4])}
    if language not in LANGUAGES:
        raise ValueError('Geçerli bir içerik dili seç.')
    if kind == 'podcast':
        with ThreadPoolExecutor(max_workers=4) as executor:
            metadata = list(executor.map(lambda item: lookup_podcast_language(item.get('itunes_id'), cache_dir), items))
        checked = [{**item, **meta} for item, meta in zip(items, metadata)]
    else:
        checked = items
    matches = [item for item in checked if item.get('language') == language]
    return matches[:4], {'requested': language, 'checked': len(checked),
                         'unknown': sum(not i.get('language') for i in checked), 'matched': len(matches)}
