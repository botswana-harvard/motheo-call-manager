from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'motheo_call_manager/home.html'
    navbar_name = 'motheo_call_manager'
    navbar_selected_item = 'home'
