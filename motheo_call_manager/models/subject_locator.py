from django.db import models
from django.utils.safestring import mark_safe
from django_crypto_fields.fields import EncryptedCharField, EncryptedTextField, FirstnameField, LastnameField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import TelephoneNumber
from edc_base.model_validators.date import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from .model_mixins import SearchSlugModelMixin
from .model_mixins import SubjectContactFieldsMixin


class LocatorManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class SubjectLocator(UniqueSubjectIdentifierFieldMixin, SiteModelMixin,
                     SubjectContactFieldsMixin, SearchSlugModelMixin, BaseUuidModel):
    """A model completed by the user to that captures participant
    locator information and permission to contact.
    """

    subject_fname = FirstnameField(
        verbose_name='First Names',
        max_length=50)

    subject_lname = LastnameField(
        verbose_name='Surname',
        max_length=50)

    report_datetime = models.DateTimeField(
        default=get_utcnow,
        validators=[datetime_not_before_study_start, datetime_not_future])

    may_call = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=mark_safe(
            'Has the participant given permission <b>to be contacted on this '
            'cell number</b>?'))

    may_call_alt = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=mark_safe(
            'Has the participant given permission <b>to be contacted on this '
            'cell number</b>?'))

    may_call_tel = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=mark_safe(
            'Has the participant given permission <b>to be contacted on this '
            'telephone number</b>?'))

    email_address = models.EmailField(
        blank=True,
        null=True,
        help_text='If no email, write None')

    may_contact_email = models.CharField(
        max_length=3,
        choices=YES_NO_NA,
        verbose_name=mark_safe(
            'Has the participant given permission <b>to be contacted by '
            'email</b>?'))

    home_village = EncryptedTextField(
        verbose_name='Home Village',
        max_length=500,
        help_text='')

    anc_clinic = models.CharField(
        verbose_name='Name of ANC Clinic',
        max_length=25,)

    may_contact_anc = models.CharField(
        verbose_name=('Has the participant given permission to be contacted, '
                      'through their ANC clinic?, if unable to contact phone numbers'),
        max_length=3,
        choices=YES_NO)

    idcc_clinic = models.CharField(
        verbose_name='Name of IDCC Clinic',
        max_length=25,
        blank=True,
        null=True)

    may_contact_idcc = models.CharField(
        verbose_name=('Has the participant given permission to be contacted, '
                      'through their IDCC clinic?, if unable to contact phone numbers'),
        max_length=3,
        choices=YES_NO_NA)

    workplace = models.CharField(
        verbose_name='Name of workplace',
        max_length=25,
        blank=True,
        null=True,
        help_text='(for those who are working)')

    work_phone = EncryptedCharField(
        verbose_name='Work Telephone',
        validators=[TelephoneNumber, ],
        blank=True,
        null=True)

    may_contact_work = models.CharField(
        verbose_name=('Has participant given permission to be contacted at their '
                      'workplace?, if unable to contact phone numbers'),
        max_length=3,
        choices=YES_NO_NA)

    next_of_kin_details = EncryptedTextField(
        verbose_name=('Name and contact details of next of kin or any individuals '
                      'participant allows us to contact if they can\'t be reached.'
                      '(can list multiple people)'),
        max_length=500,
        blank=True,
        null=True)

    loc_after_deliv = EncryptedTextField(
        verbose_name='Location participant will be staying after delivery?',
        max_length=500)

    next_ap_date = models.DateField(verbose_name='Date of follow-up visit')

    locator_review = models.CharField(
        verbose_name=('Did you review this form with the participant to '
                      'find out if there are any updates?'),
        max_length=3,
        choices=YES_NO)

    history = HistoricalRecords()

    objects = LocatorManager()

    def __str__(self):
        return '{}'.format(self.subject_identifier)

    def natural_key(self):
        return (self.subject_identifier,)
    natural_key.dependencies = ['sites.Site']

    class Meta:
        app_label = 'motheo_call_manager'
        verbose_name = 'Caregiver Locator'
