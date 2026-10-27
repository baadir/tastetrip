import os
import unittest
from unittest.mock import patch

from app.providers import flights, llm_json, normalize_entity, ProviderError


class ProviderTests(unittest.TestCase):
    def test_map_uses_google_place_id_and_unsafe_urls_are_dropped(self):
        entity = {'entity_id': 'qloo-uuid', 'name': '<Restaurant>',
                  'properties': {'address': 'Paris', 'image': {'url': 'javascript:alert(1)'},
                                 'website': 'javascript:alert(1)'},
                  'external': {'google_place': [{'place_id': 'google-id'}]}}
        normalized = normalize_entity(entity, 'restaurant')
        self.assertIn('query_place_id=google-id', normalized['map_url'])
        self.assertNotIn('qloo-uuid', normalized['map_url'])
        self.assertIsNone(normalized['image'])
        self.assertIsNone(normalized['website'])

    @patch.dict(os.environ, {'AVIASALES_API_TOKEN': 'fixture-only'})
    @patch('app.providers.request_json', return_value={'success': True, 'data': {'PAR': {
        '0': {'departure_at': '2027-01-01T12:00:00', 'return_at': '2027-01-03T12:00:00', 'price': 120},
        '1': {'departure_at': '2027-01-02T12:00:00', 'return_at': '2027-01-03T12:00:00', 'price': 50}}}})
    def test_flights_do_not_substitute_nearby_dates(self, _request):
        found = flights('IST', 'PAR', '2027-01-01', '2027-01-03')
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]['price'], 120)
        self.assertEqual(flights('IST', 'PAR', '2027-01-01'), [])

    @patch.dict(os.environ, {'LLM_API_KEY': 'fixture-only', 'LLM_MODEL': 'fixture-model'})
    @patch('app.providers.request_json', return_value={'choices': [{'message': {'content': '[]'}}]})
    def test_model_must_return_an_object(self, _request):
        with self.assertRaises(ProviderError):
            llm_json('Output JSON', 'fixture')


if __name__ == '__main__':
    unittest.main()
