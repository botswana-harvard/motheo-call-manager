from django import forms
from edc_form_validators import FormValidatorMixin

from ..form_validations import HomeVisitFormValidator
from ..models import HomeVisitAttempt


class HomeVisitAttemptForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = HomeVisitFormValidator

    class Meta:
        model = HomeVisitAttempt
        fields = '__all__'
