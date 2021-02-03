from django.apps import apps as django_apps
from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .logentry_model_wrapper import LogEntryModelWrapper


class SubjectLocatorWrapper(ModelWrapper):

    model = 'motheo_call_manager.subjectlocator'
    querystring_attrs = ['subject_identifier']
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'call_manager_listboard_url')

    @property
    def call_model_cls(self):
        return django_apps.get_model('edc_call_manager.call')

    @property
    def log_model_cls(self):
        return django_apps.get_model('edc_call_manager.log')

    @property
    def log_entry_model_cls(self):
        return django_apps.get_model('edc_call_manager.logentry')

    @property
    def call(self):
        call = self.call_model_cls.objects.filter(
            subject_identifier=self.object.subject_identifier).order_by(
                'scheduled').last()
        return str(call.id)

    @property
    def call_log(self):
        call = self.call_model_cls.objects.filter(
            subject_identifier=self.object.subject_identifier).order_by(
                'scheduled').last()
        call_log = self.log_model_cls.objects.get(call=call)
        return str(call_log.id)

    @property
    def log_entry(self):
        log = self.log_model_cls.objects.get(id=self.call_log)
        logentry = self.log_entry_model_cls(log=log)
        return LogEntryModelWrapper(logentry)

    @property
    def log_entries(self):
        call = self.call_model_cls.objects.filter(
            subject_identifier=self.subject_identifier).order_by(
                'scheduled').last()
        return self.log_entry_model_cls.objects.filter(
            log__call__subject_identifier=call.subject_identifier).order_by(
                'call_datetime')

    @property
    def contacts(self):
        contacts = []
        num_list = ['subject_cell', 'subject_cell_alt', 'subject_phone', 'subject_phone_alt']
        for contact in num_list:
            attr = getattr(self, contact, '')
            if attr:
                contacts.append(attr)
            else:
                continue
        return ', '.join(contacts)

    @property
    def call_date(self):
        latest_entry = self.log_entries.latest('call_datetime')
        return latest_entry.call_datetime

