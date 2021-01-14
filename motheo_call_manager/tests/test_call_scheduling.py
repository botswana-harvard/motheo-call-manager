from django.apps import apps as django_apps
from django.test import TestCase
from model_mommy import mommy

Call = django_apps.get_model('edc_call_manager', 'call')


class TestCallScheduling(TestCase):

    def setUp(self):
        pass

    def test_call_log_creation(self):
        mommy.make_recipe(
            'motheo_call_manager.subjectlocator',
            subject_identifier='1234')

        self.assertEqual(
            Call.objects.filter(subject_identifier='1234').count(), 1)
