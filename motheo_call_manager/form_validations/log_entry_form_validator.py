from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_constants.constants import YES, CLOSED


class LogEntryFormValidator(FormValidator):

    def clean(self):
        cleaned_data = self.cleaned_data
        log = cleaned_data.get('log')

        self.validate_other_specify(
            field='appt_location',
            required_msg=('You wrote the appointment location is OTHER, please'
                          ' specify below.'))

        fields_required = {
            'appt_date':
            ('You wrote the participant is willing to make an appointment. '
             'Please specify the appointment date.'),
            'appt_grading':
            ('You wrote the participant is willing to make an appointment. '
             'Please specify if this is a firm appointment date or not.'),
            'appt_location':
            ('You wrote the participant is willing to make an appointment. '
             'Please specify the appointment location.'), }

        for field_required, message in fields_required.items():
            self.required_if(
                YES,
                field='appt',
                field_required=field_required,
                required_msg=message)

        if log.call.call_status == CLOSED:
            message = {
                '__all__':
                'This call is closed. You may not add to or change the call log.'}
            self._errors.update(message)
            raise ValidationError(message)
