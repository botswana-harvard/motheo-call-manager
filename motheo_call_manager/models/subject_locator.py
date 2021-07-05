from django.db import models
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from django_crypto_fields.fields import EncryptedCharField, EncryptedTextField, FirstnameField, LastnameField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import date_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import date_not_before_study_start
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

    loc_admin = models.CharField(
        verbose_name='Administered by',
        max_length=50)

    first_name = FirstnameField(
        verbose_name='First Names',
        max_length=50)

    last_name = LastnameField(
        verbose_name='Surname',
        max_length=50)

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters '
                     'only in upper case, no spaces.'))],
        null=True, blank=False)

    loc_date = models.DateField(
        verbose_name='Date Completed',
        default=get_utcnow,
        validators=[date_not_before_study_start, date_not_future])

    may_call = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=mark_safe(
            'Has the participant given permission <b>to be contacted on this '
            'cell number</b>?'),
        blank=True,
        null=True)

    may_call_alt = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=mark_safe(
            'Has the participant given permission <b>to be contacted on this '
            'cell number</b>?'),
        blank=True,
        null=True)

    subject_cell_alt_3 = EncryptedCharField(
        verbose_name='Cell number (second alternate)',
        blank=True,
        null=True)

    may_call_tel = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=mark_safe(
            'Has the participant given permission <b>to be contacted on this '
            'telephone number</b>?'),
        blank=True,
        null=True)

    loc_email = models.EmailField(
        blank=True,
        null=True,
        help_text='If no email, write None')

    may_contact_email = models.CharField(
        max_length=3,
        choices=YES_NO_NA,
        verbose_name=mark_safe(
            'Has the participant given permission <b>to be contacted by '
            'email</b>?'),
        blank=True,
        null=True)

    loc_village = EncryptedTextField(
        verbose_name='Home Village',
        max_length=500,
        help_text='')

    loc_address = EncryptedTextField(
        verbose_name='Physical address with detailed description',
        max_length=500,
        blank=True,
        null=True,
        help_text='')

    may_visit_home = models.CharField(
        max_length=25,
        choices=YES_NO,
        blank=True,
        null=True,
        verbose_name=mark_safe(
            'Has the participant given permission for study '
            'staff <b>to make home visits</b> for follow-up purposes?'))

    idcc_clinic = models.CharField(
        verbose_name='Name of IDCC Clinic',
        max_length=25,
        blank=True,
        null=True)

    may_contact_idcc = models.CharField(
        verbose_name=('Has the participant given permission to be contacted, '
                      'through their IDCC clinic?, if unable to contact phone numbers'),
        max_length=3,
        choices=YES_NO_NA,
        blank=True,
        null=True)

    loc_workplace = models.CharField(
        verbose_name='Name of workplace',
        max_length=25,
        blank=True,
        null=True,
        help_text='(for those who are working)')

    loc_workphone = EncryptedCharField(
        verbose_name='Work Telephone',
        blank=True,
        null=True)

    may_contact_work = models.CharField(
        verbose_name=('Has participant given permission to be contacted at their '
                      'workplace?, if unable to contact phone numbers'),
        max_length=3,
        choices=YES_NO_NA,
        blank=True,
        null=True)

    loc_kincontact = EncryptedTextField(
        verbose_name=('Name and contact details of next of kin or any individuals '
                      'participant allows us to contact if they can\'t be reached.'
                      '(can list multiple people)'),
        max_length=500,
        blank=True,
        null=True)

    may_contact_kin = models.CharField(
        verbose_name=('Has participant given permission to contact anyone else?'
                      ' , if unable to contact phone numbers'),
        max_length=3,
        choices=YES_NO_NA,
        blank=True,
        null=True)

    date_followup = models.DateField(verbose_name='Date of follow-up visit')

    initial_call_date = models.DateField(
        verbose_name='Initial call date',
        default=get_utcnow)

    review_locator = models.CharField(
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

    def save(self, *args, **kwargs):
        if not self.initials:
            self.initials = f'{self.first_name[:1]}{self.last_name[:1]}'
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'motheo_call_manager'
        verbose_name = 'Subject Locator'
