from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls.conf import path, include
from django.views.generic.base import RedirectView
from edc_call_manager.admin_site import edc_call_manager_admin

from .admin_site import motheo_call_manager_admin

from .views import AdministrationView, HomeView

# app_name = 'motheo_call_manager'

urlpatterns = [
    path('accounts/', include('edc_base.auth.urls')),
    path('admin/', include('edc_base.auth.urls')),

    path('admin/', admin.site.urls),
    path('admin/', motheo_call_manager_admin.urls),
    path('admin/edc_call_manager', edc_call_manager_admin.urls),
    path('administration/', AdministrationView.as_view(),
         name='administration_url'),

    path('admin/motheo_call_manager', RedirectView.as_view(url='admin/'),
         name='motheo_call_manager_url'),
    path('edc_base/', include('edc_base.urls')),
    path('edc_call_manager/', include('edc_call_manager.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('edc_protocol/', include('edc_protocol.urls')),

    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='switch_sites_url'),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', HomeView.as_view(), name='home_url'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
