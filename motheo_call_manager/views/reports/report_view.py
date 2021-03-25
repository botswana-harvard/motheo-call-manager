import calendar
from datetime import datetime, timedelta, date
from django.apps import apps as django_apps
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from .scheduled_calls_calendar import ScheduledcallsCalendar


class ReportView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):

    template_name = 'motheo_call_manager/reports/call_log_entry_report.html'
    navbar_name = 'motheo_call_manager'
    navbar_selected_item = 'reports'
    model = 'motheo_call_manager.call'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('type') == 'calendar':
            d = self.get_date(self.request.GET.get('month', None))

            context.update(
                calls=self.calls,
                **self.get_extra_context(d),
                previous_month=self.prev_month(d),
                next_month=self.next_month(d),
                is_calendar=True)
        else:
            context.update(
                calls=self.calls,
                is_report=True)
        return context

    @property
    def calls(self):
        call_model_cls = django_apps.get_model(self.model)
        return call_model_cls.objects.all()

    def get_date(self, req_month):
        if req_month:
            year, month = (int(x) for x in req_month.split('-'))
            return date(year, month, day=1)
        return datetime.today()

    def prev_month(self, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        month = '?type=calendar&month=' + str(prev_month.year) + '-' + str(prev_month.month)
        return month

    def next_month(self, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = '?type=calendar&month=' + str(next_month.year) + '-' + str(next_month.month)
        return month

    def get_extra_context(self, month_year):

        after_day = None  # request.GET.get('day__gte', None)
        extra_context = {}

        if not after_day:
            d = month_year or date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = date.today()
        cal = ScheduledcallsCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return extra_context
