from django import forms
from edc_form_validators import FormValidatorMixin

from ..form_validations import LogEntryFormValidator
from ..models import LogEntry


class LogEntryForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = LogEntryFormValidator

    class Meta:
        model = LogEntry
        fields = '__all__'
