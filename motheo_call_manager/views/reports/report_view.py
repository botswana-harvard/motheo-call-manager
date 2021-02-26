from django.apps import apps as django_apps
from django.contrib import admin
import datetime
import calendar
from django.urls.base import reverse
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
        context.update(
            calls=self.calls,
            **self.get_extra_context())
        return context

    @property
    def calls(self):
        call_model_cls = django_apps.get_model(self.model)
        return call_model_cls.objects.all()

    def get_extra_context(self):

        after_day = None  # request.GET.get('day__gte', None)
        extra_context = {}

        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()

        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month

        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month

#         extra_context['previous_month'] = reverse('admin:events_event_changelist') + '?day__gte=' + str(
#             previous_month)
#         extra_context['next_month'] = reverse('admin:events_event_changelist') + '?day__gte=' + str(next_month)

        cal = ScheduledcallsCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return extra_context
