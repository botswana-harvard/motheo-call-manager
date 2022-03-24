from django.contrib import admin
from edc_call_manager.admin import ModelAdminCallMixin, ModelAdminLogEntryMixin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import motheo_call_manager_admin
from ..models import Call, Log, LogEntry, CallLogEntry
from ..forms import LogEntryForm, CallLogEntryForm


@admin.register(CallLogEntry, site=motheo_call_manager_admin)
class CallLogEntryAdmin(ModelAdminMixin, ModelAdminCallMixin, admin.ModelAdmin):
    pass


@admin.register(Call, site=motheo_call_manager_admin)
class CallAdmin(ModelAdminMixin, ModelAdminCallMixin, admin.ModelAdmin):
    pass


@admin.register(Log, site=motheo_call_manager_admin)
class LogAdmin(ModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(LogEntry, site=motheo_call_manager_admin)
class LogEntryAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = LogEntryForm

    search_fields = ['study_maternal_identifier']

    date_hierarchy = 'appt_date'

    fieldsets = (
        (None, {
            'fields': (
                'log',
                'call_reason',
                'call_datetime',
                'contact_type',
                'time_of_week',
                'time_of_day',
                'appt',
                'appt_reason_unwilling',
                'appt_reason_unwilling_other',
                'appt_date',
                'appt_grading',
                'appt_location',
                'appt_location_other',
                'may_call',
            )},
         ),
        audit_fieldset_tuple
    )

    radio_fields = {
        'call_reason': admin.VERTICAL,
        'contact_type': admin.VERTICAL,
        'time_of_week': admin.VERTICAL,
        'time_of_day': admin.VERTICAL,
        'appt': admin.VERTICAL,
        'appt_reason_unwilling': admin.VERTICAL,
        'appt_grading': admin.VERTICAL,
        'appt_location': admin.VERTICAL,
        'may_call': admin.VERTICAL,
    }

    list_display = (
        'log',
        'call_datetime',
        'appt',
        'appt_date',
        'may_call',
    )

    list_filter = (
        'call_datetime',
        'appt',
        'appt_date',
        'may_call',
        'created',
        'modified',
        'hostname_created',
        'hostname_modified',
    )

    search_fields = ('id', 'log__call__subject_identifier')

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['log'].queryset = \
            Log.objects.filter(id=request.GET.get('log'))
        return super(LogEntryAdmin, self).render_change_form(
            request, context, *args, **kwargs)
