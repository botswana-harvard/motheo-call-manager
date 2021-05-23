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
                'loc_admin',
                'loc_date',
                'first_name',
                'last_name',
                'initials',
                'subject_cell',
                'may_call',
                'subject_cell_alt',
                'subject_cell_alt_3',
                'may_call_alt',
                'subject_phone',
                'may_call_tel',
                'loc_email',
                'may_contact_email',
                'may_sms',
                'loc_village',
                'loc_address',
                'may_visit_home',
                'idcc_clinic',
                'may_contact_idcc',
                'loc_workplace',
                'loc_workphone',
                'may_contact_work',
                'loc_kincontact',
                'may_contact_kin',
                'date_followup',
                'initial_call_date',
                'review_locator'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'may_call': admin.VERTICAL,
                    'may_sms': admin.VERTICAL,
                    'may_call_alt': admin.VERTICAL,
                    'may_call_tel': admin.VERTICAL,
                    'may_contact_email': admin.VERTICAL,
                    'may_visit_home': admin.VERTICAL,
                    'may_contact_idcc': admin.VERTICAL,
                    'may_contact_work': admin.VERTICAL,
                    'review_locator': admin.VERTICAL}

    search_fields = ['subject_identifier']

    list_display = ('subject_identifier', 'loc_date', 'first_name', 'last_name')

