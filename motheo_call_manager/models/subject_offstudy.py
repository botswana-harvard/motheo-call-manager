from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.model_validators.date import datetime_not_future
from edc_base.sites import SiteModelFormMixin
from edc_base.utils import get_utcnow
from edc_identifier.managers import SubjectIdentifierManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import date_not_before_study_start
from edc_protocol.validators import datetime_not_before_study_start

from ..choices import OFF_STUDY_REASON


class SubjectOffStudy(UniqueSubjectIdentifierFieldMixin, SiteModelFormMixin, BaseUuidModel):
    """A model completed by the user that completed when the
    subject is taken off-study.
    """

    offstudy_date = models.DateField(
        verbose_name="Off-study Date",
        null=True,
        default=get_utcnow,
        validators=[
            date_not_before_study_start,
            date_not_future])

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        null=True,
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    last_contact = models.DateField(
        verbose_name='Date of last contact',
        default=get_utcnow,
        validators=[
            date_not_before_study_start,
            date_not_future])

    reason = models.TextField(
        verbose_name='Describe the primary reason for going offstudy',
        max_length=500,
        null=True)

    reason_code = models.CharField(
        verbose_name=('Based on the description above code the primary reason '
                      'for the participant to be going offstudy'),
        max_length=150,
        choices=OFF_STUDY_REASON,
        null=True)

    reason_code_other = OtherCharField()

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment",
        blank=True,
        null=True)

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    class Meta:
        app_label = 'motheo_call_manager'
        verbose_name_plural = 'Subject Off Study'
