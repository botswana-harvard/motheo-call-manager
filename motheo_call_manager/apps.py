from datetime import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz

from django.apps import AppConfig as DjangoAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig


class AppConfig(DjangoAppConfig):
    name = 'motheo_call_manager'
    verbose_name = 'Motheo Call Manager'
    admin_site_name = 'motheo_call_manager_admin'

    def ready(self):
        from .models import call_on_post_save


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Motheo Call Manager'
    institution = 'Botswana-Harvard AIDS Institute'


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = '134'


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP134'
    protocol_name = 'Motheo Call Manager'
    protocol_number = '134'
    protocol_title = ''
    study_open_datetime = datetime(
        2020, 3, 1, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(
        2025, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))


class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
    country = 'botswana'
    definitions = {
        '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                             slots=[100, 100, 100, 100, 100, 100, 100]),
        '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                             slots=[100, 100, 100, 100, 100])}
