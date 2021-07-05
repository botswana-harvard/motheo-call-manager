from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import motheo_call_manager_admin

app_name = 'motheo_call_manager'

urlpatterns = [
    path('admin/', motheo_call_manager_admin.urls),
    path('', RedirectView.as_view(url='admin/'), name='home_url'),
]
