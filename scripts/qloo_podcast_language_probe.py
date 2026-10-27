"""Read-only language experiments; no credentials or raw payloads persisted."""
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')
BASE = os.getenv('QLOO_API_URL', 'https://hackathon.api.qloo.com')
COMMON = {'filter.type': 'urn:entity:podcast', 'take': 5,
          'signal.interests.entities': 'C1EDF39B-AC56-4130-B881-AD93794D9367'}


def language_fields(value, prefix=''):
    found = {}
    if isinstance(value, dict):
        for k, v in value.items():
            path = prefix + '.' + k
            if 'lang' in k.lower():
                found[path] = v
            elif isinstance(v, (dict, list)):
                found.update(language_fields(v, path))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            found.update(language_fields(item, prefix + '[' + str(i) + ']'))
    return found


def probe(case):
    name, path, params = case
    try:
        response = requests.get(BASE + path, headers={'X-Api-Key': os.environ['QLOO_API_KEY']},
                                params=params, timeout=30)
        try:
            data = response.json()
        except ValueError:
            data = {}
        result = {'case': name, 'parameters': params, 'http': response.status_code}
        if response.status_code != 200:
            result['diagnostic'] = {k: data[k] for k in ('error', 'errors', 'message') if k in data}
            return result
        rows = (data.get('results') or {}).get('entities', [])
        tags = (data.get('results') or {}).get('tags', [])
        result.update(ids=[e.get('entity_id') for e in rows], names=[e.get('name') for e in rows],
                      language_fields=[language_fields(e) for e in rows],
                      property_keys=sorted(set(k for e in rows for k in (e.get('properties') or {}))),
                      external_keys=sorted(set(k for e in rows for k in (e.get('external') or {}))),
                      language_tags=[t for e in rows for t in e.get('tags', []) if 'language' in t.get('id', '')],
                      tags=[{'id': t.get('id'), 'name': t.get('name')} for t in tags])
        return result
    except requests.RequestException:
        return {'case': name, 'http': None, 'error': 'Network request failed'}


if __name__ == '__main__':
    cases = [('baseline', '/v2/insights', COMMON)]
    for key, values in [('language', ['tr', 'en', 'zz']), ('filter.language', ['tr', 'en', 'zz']),
                        ('filter.languages', ['tr']), ('filter.language_code', ['tr'])]:
        for value in values:
            cases.append((key + '=' + value, '/v2/insights', {**COMMON, key: value}))
    for text in ['Turkish', 'English', 'language', 'Turkish language']:
        cases.append(('tag-search:' + text, '/v2/tags', {'filter.query': text,
                     'filter.parents.types': 'urn:entity:podcast', 'take': 10}))
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(probe, cases))
    results.append(probe(('baseline-repeat', '/v2/insights', COMMON)))
    baseline = results[0].get('ids')
    for r in results:
        if 'ids' in r and r['case'].startswith(('language', 'filter.', 'baseline')):
            r['same_order_as_baseline'] = r['ids'] == baseline
    output = {'date': '2026-10-21', 'calls': len(results), 'results': results}
    path = Path('docs/validation/qloo-podcast-language-2026-10-21.json')
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    for r in results:
        print(json.dumps({k: r[k] for k in ['case', 'http', 'diagnostic', 'same_order_as_baseline', 'tags',
                                            'property_keys', 'external_keys'] if k in r}, ensure_ascii=True))
