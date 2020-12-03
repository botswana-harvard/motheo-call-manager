from django.contrib import admin
from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import motheo_call_manager_admin
from ..forms import SubjectOffStudyForm
from ..models import SubjectOffStudy
from .modeladmin_mixins import ModelAdminMixin


@admin.register(SubjectOffStudy, site=motheo_call_manager_admin)
class SubjectOffStudyAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SubjectOffStudyForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'offstudy_date',
                'last_contact',
                'reason',
                'reason_code',
                'reason_code_other'
                'comment']}
         ), audit_fieldset_tuple)

    radio_fields = {
        'reason_code': admin.VERTICAL,
    }

    search_fields = ['subject_identifier']

    list_display = ('subject_identifier', 'offstudy_date')
