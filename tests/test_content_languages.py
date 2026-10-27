import socket
import tempfile
import unittest
from unittest.mock import patch

from app.content_languages import (filter_content_language, normalize_language, public_target,
                                   rss_language, lookup_podcast_language)


class LanguageTests(unittest.TestCase):
    def test_language_codes_and_unknown(self):
        self.assertEqual(normalize_language('tr-TR'), 'tr')
        self.assertEqual(normalize_language('English'), 'en')
        self.assertIsNone(normalize_language('unknown'))

    def test_rss_language_is_channel_not_description(self):
        xml = b'<rss><channel><description>Turkish</description><language>en-US</language></channel></rss>'
        self.assertEqual(rss_language(xml), 'en')

    def test_xml_entity_expansion_is_rejected(self):
        from defusedxml.common import DefusedXmlException
        with self.assertRaises(DefusedXmlException):
            rss_language(b'<!DOCTYPE rss [<!ENTITY a "en">]><rss><channel><language>&a;</language></channel></rss>')

    @patch('app.content_languages.socket.getaddrinfo', return_value=[(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', 80))])
    def test_private_network_and_ports_are_blocked(self, _resolve):
        for url in ['http://localhost/feed', 'http://127.0.0.1/feed', 'http://example.com:8080/feed',
                    'file:///etc/passwd', 'https://user:password@example.com/feed']:
            with self.assertRaises(ValueError):
                public_target(url)

    def test_book_language_filter_does_not_include_unknown_or_other_languages(self):
        items = [{'id': 'a', 'language': 'tr'}, {'id': 'b', 'language': 'en'}, {'id': 'c', 'language': None}]
        result, stats = filter_content_language(items, 'book', 'tr', '.')
        self.assertEqual([x['id'] for x in result], ['a'])
        self.assertEqual(stats['unknown'], 1)

    @patch('app.content_languages.read_public', side_effect=[
        b'{"results":[{"collectionId":123,"feedUrl":"https://example.com/feed"}]}', 'tr'])
    def test_verified_rss_language_is_cached(self, fetch):
        with tempfile.TemporaryDirectory() as directory:
            first = lookup_podcast_language('123', directory)
            second = lookup_podcast_language('123', directory)
            self.assertEqual(first['language'], 'tr')
            self.assertEqual(first, second)
            self.assertEqual(fetch.call_count, 2)

    @patch('app.content_languages.read_public', side_effect=[
        b'{"results":[{"collectionId":123,"collectionViewUrl":"https://podcasts.apple.com/us/podcast/example/id123","feedUrl":"https://example.com/feed"}]}',
        ValueError('RSS unavailable')])
    def test_apple_link_survives_failed_language_lookup(self, _fetch):
        with tempfile.TemporaryDirectory() as directory:
            result = lookup_podcast_language('123', directory)
            self.assertIsNone(result['language'])
            self.assertEqual(result['apple_url'], 'https://podcasts.apple.com/us/podcast/example/id123')

    @patch('app.content_languages.lookup_podcast_language', side_effect=[{'language': 'en'}, {'language': None}])
    def test_no_silent_language_relaxation(self, _lookup):
        result, stats = filter_content_language([{'itunes_id': '1'}, {'itunes_id': '2'}], 'podcast', 'tr', '.')
        self.assertEqual(result, [])
        self.assertEqual(stats['matched'], 0)
        self.assertEqual(stats['unknown'], 1)
