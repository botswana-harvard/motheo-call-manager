from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'motheo_call_manager'
    verbose_name = 'Motheo Call Manager'
    admin_site_name = 'motheo_call_manager_admin'
