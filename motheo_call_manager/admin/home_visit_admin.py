from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import motheo_call_manager_admin
from ..forms import HomeVisitAttemptForm
from ..models import HomeVisitAttempt, HomeVisit


@admin.register(HomeVisitAttempt, site=motheo_call_manager_admin)
class HomeVisitAttemptAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = HomeVisitAttemptForm

    date_hierarchy = 'appt_date'

    fieldsets = (
        (None, {
            'fields': (
                'home_visit',
                'contact_attempted',
                'contact_staff',
                'contact_date',
                'contact_loc',
                'contact_outcome',
                'appt',
                'appt_date',
                'offstudy',
                'comment',
            )},
         ),
        audit_fieldset_tuple
    )

    radio_fields = {
        'contact_attempted': admin.VERTICAL,
        'appt': admin.VERTICAL,
        'offstudy': admin.VERTICAL
    }

    list_display = (
        'home_visit',
        'contact_date',
        'contact_loc',
        'contact_outcome',
        'appt_date',
    )

    list_filter = (
        'contact_date',
        'appt',
        'appt_date',
        'created',
        'modified',
        'hostname_created',
        'hostname_modified',
    )

    search_fields = ('contact_date', 'home_visit__subject_identifier')

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['home_visit'].queryset = \
            HomeVisit.objects.filter(id=request.GET.get('home_visit'))
        return super(HomeVisitAttemptAdmin, self).render_change_form(
            request, context, *args, **kwargs)
