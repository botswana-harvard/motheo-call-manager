from django.db import models
from django.db.models.deletion import PROTECT
from django_crypto_fields.fields import EncryptedTextField, FirstnameField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future, date_is_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO


class HomeVisit(BaseUuidModel):

    subject_identifier = models.CharField(max_length=50)

    scheduled_date = models.DateField(default=get_utcnow)

    history = HistoricalRecords()

    def __str__(self):
        return self.subject_identifier

    class Meta:
        app_label = 'motheo_call_manager'


class HomeVisitAttempt(BaseUuidModel):

    home_visit = models.ForeignKey(
        HomeVisit,
        on_delete=PROTECT)

    contact_attempted = models.CharField(
        verbose_name='Was a home visit attempt made?',
        choices=YES_NO,
        max_length=3)

    contact_staff = FirstnameField(
        verbose_name='Name(s) of staff member who visited the participant',
        blank=True,
        null=True)

    contact_date = models.DateField(
        verbose_name='Date of home visit attempt',
        validators=[date_not_future, ],
        blank=True,
        null=True)

    contact_loc = EncryptedTextField(
        verbose_name='Which address was used for contact attempt?',
        max_length=500,
        help_text='Provide a detailed description of the physical address.',
        blank=True,
        null=True)

    contact_outcome = models.TextField(
        verbose_name='What was the outcome of the in person visit.',
        max_length=500,
        null=True,
        blank=True)

    appt = models.CharField(
        verbose_name='Is the participant willing to schedule an appointment',
        max_length=7,
        choices=YES_NO,
        null=True,
        blank=True)

    appt_date = models.DateField(
        verbose_name='Appointment Date',
        validators=[date_is_future],
        null=True,
        blank=True,
        help_text='This can only come from the participant.')

    offstudy = models.CharField(
        verbose_name='Is the participant going offstudy?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    comment = models.TextField(
        verbose_name='Additional Comments',
        blank=True,
        null=True)

    class Meta:
        app_label = 'motheo_call_manager'
