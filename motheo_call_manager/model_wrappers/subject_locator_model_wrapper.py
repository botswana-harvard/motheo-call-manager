from django.apps import apps as django_apps
from django.conf import settings
from edc_base.utils import get_utcnow
from edc_model_wrapper import ModelWrapper

from .home_visit_model_wrapper import HomeVisitAttemptModelWrapper
from .logentry_model_wrapper import LogEntryModelWrapper


class SubjectLocatorWrapper(ModelWrapper):

    model = 'motheo_call_manager.subjectlocator'
    querystring_attrs = ['subject_identifier']
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'call_manager_listboard_url')

    @property
    def call_model_cls(self):
        return django_apps.get_model('motheo_call_manager.call')

    @property
    def log_model_cls(self):
        return django_apps.get_model('motheo_call_manager.log')

    @property
    def log_entry_model_cls(self):
        return django_apps.get_model('motheo_call_manager.logentry')

    @property
    def home_visit_attempt_model_cls(self):
        return django_apps.get_model('motheo_call_manager.homevisitattempt')

    @property
    def home_visit_model_cls(self):
        return django_apps.get_model('motheo_call_manager.homevisit')

    @property
    def call(self):
        call = self.call_model_cls.objects.filter(
            subject_identifier=self.object.subject_identifier).latest('scheduled')
        return str(call.id)

    @property
    def call_log(self):
        call = self.call_model_cls.objects.filter(
            subject_identifier=self.object.subject_identifier).latest('scheduled')
        call_log = self.log_model_cls.objects.get(call=call)
        return str(call_log.id)

    @property
    def log_entry(self):
        log = self.log_model_cls.objects.get(id=self.call_log)
        logentry = self.log_entry_model_cls(log=log)
        return LogEntryModelWrapper(logentry)

    @property
    def log_entries(self):
        wrapped_entries = []
        call = self.call_model_cls.objects.filter(
            subject_identifier=self.subject_identifier).latest('scheduled')
        subject_identifier = call.subject_identifier if call else ''
        log_entries = self.log_entry_model_cls.objects.filter(
            log__call__subject_identifier=subject_identifier).order_by(
                '-call_datetime')[:3]
        for log_entry in log_entries:
            wrapped_entries.append(
                LogEntryModelWrapper(log_entry))
        return wrapped_entries

    @property
    def home_visit_attempts(self):
        wrapped_entries = []
        contact_attempts = []
        home_visit = self.home_visit_model_cls.objects.filter(
            subject_identifier=self.subject_identifier).latest('scheduled_date')
        if home_visit:
            contact_attempts = self.home_visit_attempt_model_cls.objects.filter(
                home_visit=home_visit)
        for attempt in contact_attempts:
            wrapped_entries.append(
                HomeVisitAttemptModelWrapper(attempt))

        return wrapped_entries

    @property
    def home_visit_attempt(self):
        home_visit = self.home_visit_model_cls.objects.filter(
            subject_identifier=self.subject_identifier).latest('scheduled_date')
        home_visit_attempt = self.home_visit_attempt_model_cls(
            home_visit=home_visit)
        return HomeVisitAttemptModelWrapper(home_visit_attempt)

    @property
    def home_visit_required(self):
        call_attempts = self.log_entry_model_cls.objects.filter(
            log__call__subject_identifier=self.subject_identifier,
            call_datetime__month=get_utcnow().month).order_by('-call_datetime')
        if len(call_attempts) > 4:
            latest_entries = call_attempts[:5]
            return all(entry.contact_type == 'no_contact' for entry in latest_entries)
        return False

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
        call = self.call_model_cls.objects.filter(
            subject_identifier=self.subject_identifier).order_by(
                'scheduled').last()
        subject_identifier = call.subject_identifier if call else ''
        log_entry = self.log_entry_model_cls.objects.filter(
            log__call__subject_identifier=subject_identifier).latest('call_datetime')
        return log_entry.call_datetime
