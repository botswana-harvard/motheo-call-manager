from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import motheo_call_manager_admin
from ..forms import EnrollmentChecklistForm
from ..models import EnrollmentChecklist
from .modeladmin_mixins import ModelAdminMixin


@admin.register(EnrollmentChecklist, site=motheo_call_manager_admin)
class EnrollmentChecklistAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = EnrollmentChecklistForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'maternal_dob',
                'maternal_age',
                'age_of_consent',
                'informed_consent',
                'followup_consent',
                'remain_in_area',
                'keep_contact',
                'nationality',
                'incarcerated',
                'hiv_neg_doc',
                'hiv_pos_doc',
                'efv_art_regimen',
                'dtg_art_regimen',
                'child_dob',
                'child_age',
                'child_is_of_age',
                'child_hiv_neg',
                'child_test_date',
                'child_test_type',
                'child_test_type_other',
                'team_performed_test',
                'add_reasons_ineligible',
                'specify_reasons',
                'consent_discussed',
                'consent_review',
                'consent_signed',
                'consent_samples',
                'consent_copy',
                'consent_received'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'age_of_consent': admin.VERTICAL,
                    'informed_consent': admin.VERTICAL,
                    'followup_consent': admin.VERTICAL,
                    'remain_in_area': admin.VERTICAL,
                    'keep_contact': admin.VERTICAL,
                    'nationality': admin.VERTICAL,
                    'incarcerated': admin.VERTICAL,
                    'hiv_neg_doc': admin.VERTICAL,
                    'hiv_pos_doc': admin.VERTICAL,
                    'efv_art_regimen': admin.VERTICAL,
                    'dtg_art_regimen': admin.VERTICAL,
                    'child_is_of_age': admin.VERTICAL,
                    'child_hiv_neg': admin.VERTICAL,
                    'child_test_type': admin.VERTICAL,
                    'team_performed_test': admin.VERTICAL,
                    'add_reasons_ineligible': admin.VERTICAL,
                    'consent_discussed': admin.VERTICAL,
                    'consent_review': admin.VERTICAL,
                    'consent_signed': admin.VERTICAL,
                    'consent_samples': admin.VERTICAL,
                    'consent_copy': admin.VERTICAL,
                    'consent_received': admin.VERTICAL, }

    search_fields = ['subject_identifier']

    list_display = ('subject_identifier', )
