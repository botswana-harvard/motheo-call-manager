import json
from django.test import TestCase, Client
from django.urls.base import reverse
from rest_framework import status

from ..models import SubjectLocator

# initialize the APIClient app
client = Client()


class TestCreateLocator(TestCase):

    def setUp(self):
        self.valid_payload = {
            'redcap_url': 'http://localhost:90/redcap/',
            'project_url': 'http://localhost:90/redcap/redcap_v8.9.1/index.php?pid=18',
            'project_id': '18',
            'username': 'adiphoko',
            'record': '1',
            'instrument': 'locator_form',
            'locator_form_complete': '2'
        }

        self.invalid_payload = {
            'redcap_url': 'http://localhost:90/redcap/',
            'project_url': 'http://localhost:90/redcap/redcap_v8.9.1/index.php?pid=18',
            'project_id': '18',
            'username': 'adiphoko',
            'record': '0',
            'instrument': 'locator',
            'locator_form_complete': '2'
        }

    def test_create_valid_locator(self):
        response = client.post(
            reverse('redcap_trigger_receive'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(
            SubjectLocator.objects.all().count(), 1)

    def test_create_invalid_locator(self):
        response = client.post(
            reverse('redcap_trigger_receive'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.data, {})
