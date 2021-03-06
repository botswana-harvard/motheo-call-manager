from django.conf import settings
from edc_model_wrapper import ModelWrapper


class LogEntryModelWrapper(ModelWrapper):

    model = 'motheo_call_manager.logentry'
    querystring_attrs = ['log', 'subject_identifier']
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'call_manager_listboard_url')

    @property
    def log(self):
        return self.object.log

    @property
    def subject_identifier(self):
        return self.object.log.call.subject_identifier
