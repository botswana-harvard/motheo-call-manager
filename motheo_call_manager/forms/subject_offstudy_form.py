from django import forms
from ..models import SubjectOffStudy


class SubjectOffStudyForm(forms.ModelForm):

    class Meta:
        model = SubjectOffStudy
        fields = '__all__'
