from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ..models import SubjectLocator, Call


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'motheo_call_manager/home.html'
    navbar_name = 'motheo_call_manager'
    navbar_selected_item = 'home'

    @property
    def total_locators(self):
        """Return all motheo locators count"""
        return SubjectLocator.objects.all().count()

    @property
    def total_scheduled_calls(self):
        """Return all motheo scheduled calls count"""
        return Call.objects.all().count()

    @property
    def total_subjects_called(self):
        """Return all successful calls to motheo participant"""
        called = Call.objects.filter(
            call_datetime__isnull=False, call_status='closed')
        return called.count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            total_locators=self.total_locators,
            total_calls=self.total_scheduled_calls,
            total_called=self.total_subjects_called)
        return context
