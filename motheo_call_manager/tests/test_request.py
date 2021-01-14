from django.test import TestCase

from ..classes import RedcapAPIError, RedcapRequest


class TestRequest(TestCase):

    def setUp(self):
        self.url = 'http://localhost:90/redcap/'

        self.base = {
            'token': 'D874A77F93C02D81BD6D09262411BD4B',
            'format': 'json',
            'type': 'flat',
        }

    def test_req_fields_missing(self):
        """Test that RedcapRequest raises errors for incorrect payload"""
        payload = self.base
        args = [self.url, payload, 'exp_record']

        #  no 'content' key
        self.assertRaises(RedcapAPIError, RedcapRequest, *args)

        #  good content
        payload['content'] = 'record'
        resp = RedcapRequest(*args)
        self.assertIsInstance(resp, RedcapRequest)

    def test_export_records_content(self):
        """Test that export for records checks for proper content"""
        payload = {
            'token': 'foobar',
            'content': 'record',
            'format': 'json',
            'type': 'flat'
        }
        url = self.url
        r_type = 'exp_record'

        RedcapRequest(url, payload, r_type)

        # This should raise because of a different content
        payload['content'] = 'foobar'
        with self.assertRaises(RedcapAPIError):
            RedcapRequest(url, payload, r_type)
