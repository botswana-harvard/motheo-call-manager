from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import motheo_call_manager_admin
from ..forms import SubjectLocatorForm
from ..models import SubjectLocator
from .modeladmin_mixins import ModelAdminMixin


@admin.register(SubjectLocator, site=motheo_call_manager_admin)
class SubjectLocatorAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SubjectLocatorForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'subject_fname',
                'subject_lname',
                'subject_cell',
                'may_call',
                'subject_cell_alt',
                'may_call_alt',
                'subject_phone',
                'may_call_tel',
                'email_address',
                'may_contact_email',
                'home_village',
                'physical_address',
                'may_visit_home',
                'anc_clinic',
                'may_contact_anc',
                'idcc_clinic',
                'may_contact_idcc',
                'workplace',
                'work_phone',
                'may_contact_work',
                'next_of_kin_details',
                'loc_after_deliv',
                'next_ap_date',
                'locator_review'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'may_call': admin.VERTICAL,
                    'may_call_alt': admin.VERTICAL,
                    'may_call_tel': admin.VERTICAL,
                    'may_contact_email': admin.VERTICAL,
                    'may_visit_home': admin.VERTICAL,
                    'may_contact_anc': admin.VERTICAL,
                    'may_contact_idcc': admin.VERTICAL,
                    'may_contact_work': admin.VERTICAL,
                    'locator_review': admin.VERTICAL}

    search_fields = ['subject_identifier']

    list_display = ('subject_identifier', )
