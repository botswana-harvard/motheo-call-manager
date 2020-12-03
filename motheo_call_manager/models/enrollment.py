from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_protocol.validators import datetime_not_before_study_start

from .enrollment_model_mixin import EnrollmentMixin


class EnrollmentChecklistManager(models.Manager):
    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class EnrollmentChecklist(EnrollmentMixin, SiteModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=360)

    report_datetime = models.DateTimeField(
        default=get_utcnow,
        validators=[datetime_not_before_study_start, datetime_not_future])

    maternal_dob = models.DateField(
        verbose_name='Maternal Date of birth',)

    maternal_age = models.IntegerField()

    age_of_consent = models.CharField(
        verbose_name='Mother is atleast 18 years of age',
        choices=YES_NO,
        max_length=3)

    informed_consent = models.CharField(
        verbose_name=('Mother is willing and able to provide written informed '
                      'consent for her and her child\'s participation in the study'),
        choices=YES_NO,
        max_length=3)

    followup_consent = models.CharField(
        verbose_name=('Mother is willing and able to follow up (with her child)'
                      ' for 3years'),
        choices=YES_NO,
        max_length=3)

    remain_in_area = models.CharField(
        verbose_name=('Mother intends to remain in the general Gaborone area '
                      'for the duration of the study'),
        choices=YES_NO,
        max_length=3)

    keep_contact = models.CharField(
        verbose_name=('Mother is willing to stay in telephone contact with the '
                      'study team between the 2- and 5-year visits'),
        choices=YES_NO,
        max_length=3)

    nationality = models.CharField(
        verbose_name=('Mother is documented to be a Botswana citizen'),
        choices=YES_NO,
        max_length=3)

    incarcerated = models.CharField(
        verbose_name=('Mother is currently involuntarily incarcerated'),
        choices=YES_NO,
        max_length=3)

    objects = EnrollmentChecklistManager()

    def natural_key(self):
        return(self.subject_identifier, )
    natural_key.dependencies = ['sites.Site']

    class Meta:
        app_label = 'motheo_call_manager'
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollment"
