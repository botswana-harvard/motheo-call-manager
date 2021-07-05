from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls.conf import path, include
from django.views.generic.base import RedirectView
from edc_call_manager.admin_site import edc_call_manager_admin
from edc_dashboard import UrlConfig

from .admin_site import motheo_call_manager_admin

from .views import AdministrationView, HomeView, TriggerView, ListboardView
from .views import ReportView

app_name = 'motheo_call_manager'

urlpatterns = [
    path('accounts/', include('edc_base.auth.urls')),
    path('admin/', include('edc_base.auth.urls')),

    path('admin/', admin.site.urls),

    path('admin/', motheo_call_manager_admin.urls),
    path('admin/edc_call_manager/', edc_call_manager_admin.urls),

    path('administration/', AdministrationView.as_view(),
         name='administration_url'),

    path('admin/motheo_call_manager/',
         RedirectView.as_view(url='admin/motheo_call_manager/'),
         name='motheo_call_manager_url'),
    path('motheo_call_manager/', include('motheo_call_manager.main_urls')),

    path('edc_base/', include('edc_base.urls')),
    path('edc_call_manager/', include('edc_call_manager.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('edc_protocol/', include('edc_protocol.urls')),

    path('api/redcap_trigger_receive/', TriggerView.as_view(), name='redcap_trigger_receive'),

    path('motheo_call_manager/reports/', ReportView.as_view(), name='report_url'),

    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='switch_sites_url'),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', HomeView.as_view(), name='home_url'),
]

call_manager_listboard_url_config = UrlConfig(
    url_name='call_manager_listboard_url',
    view_class=ListboardView,
    label='call_manager_listboard',
    identifier_label='subject_identifier',
    identifier_pattern='')

urlpatterns += call_manager_listboard_url_config.listboard_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
