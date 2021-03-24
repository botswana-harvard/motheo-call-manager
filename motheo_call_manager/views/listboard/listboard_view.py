import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin

from ...model_wrappers import SubjectLocatorWrapper


class ListboardView(NavbarViewMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    BaseListboardView):

    listboard_template = 'call_manager_listboard_template'
    listboard_url = 'call_manager_listboard_url'
    listboard_panel_style = 'success'
    listboard_fa_icon = "far fa-user-circle"

    model = 'motheo_call_manager.subjectlocator'
    model_wrapper_cls = SubjectLocatorWrapper
    navbar_name = 'motheo_call_manager'
    navbar_selected_item = 'call_manager'
    search_form_url = 'call_manager_listboard_url'

    @property
    def all_calls(self):
        log_entry_model_cls = django_apps.get_model(
            'motheo_call_manager.logentry')
        all_calls = log_entry_model_cls.objects.values_list(
            'log__call__subject_identifier', flat=True).all().distinct().count()
        return all_calls

    @property
    def all_subject_locators(self):
        subject_locator_cls = django_apps.get_model(
            'motheo_call_manager.subjectlocator')
        all_locators = subject_locator_cls.objects.all().count()
        return all_locators

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            all_calls=self.all_calls,
            all_subject_locators=self.all_subject_locators
        )
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
