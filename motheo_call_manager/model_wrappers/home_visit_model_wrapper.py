from django.conf import settings

from edc_model_wrapper.wrappers import ModelWrapper


class HomeVisitAttemptModelWrapper(ModelWrapper):

    model = 'motheo_call_manager.homevisitattempt'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'call_manager_listboard_url')
    querystring_attrs = ['home_visit', 'subject_identifier']
    next_url_attrs = ['subject_identifier']

    @property
    def subject_identifier(self):
        return self.object.home_visit.subject_identifier

    @property
    def home_visit(self):
        return self.object.home_visit.id
