from edc_form_validators import FormValidator
from edc_constants.constants import YES


class HomeVisitFormValidator(FormValidator):

    def clean(self):
        self.validate_required_fields()

    def validate_required_fields(self):
        fields_required = ['contact_staff', 'contact_date', 'contact_loc',
                           'contact_outcome', 'appt', 'offstudy']
        for field in fields_required:
            self.required_if(
                YES,
                field='contact_attempted',
                field_required=field)

        self.required_if(
                YES,
                field='appt',
                field_required='appt_date')
