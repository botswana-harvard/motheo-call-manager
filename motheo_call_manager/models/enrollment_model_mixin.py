from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from ..choices import TEST_TYPES


class EnrollmentMixin(models.Model):

    hiv_neg_doc = models.CharField(
        verbose_name=('Mother has documentation of negative HIV-1 status '
                      'during or after pregnancy with the child who will be '
                      'enrolled into Motheo'),
        choices=YES_NO,
        max_length=3)

    hiv_pos_doc = models.CharField(
        verbose_name=('Mother has documentation of positive HIV-1 status '
                      'during or after pregnancy with the child who will be '
                      'enrolled into Motheo'),
        choices=YES_NO,
        max_length=3)

    efv_art_regimen = models.CharField(
        verbose_name=('Mother has documented history of treatment with '
                      'EFV/TDF/3TC or EFV/TDF/FTC while pregnant with the '
                      'child who will be enrolled into motheo'),
        choices=YES_NO,
        max_length=3)

    dtg_art_regimen = models.CharField(
        verbose_name=('Mother has documented history of treatment with '
                      'DTG/TDF/3TC or DTG/TDF/FTC while pregnant with the '
                      'child who will be enrolled into motheo'),
        choices=YES_NO,
        max_length=3)

    confirm_enrol = models.CharField(
        verbose_name=('Did you confirm that we still need to enroll women from '
                      'this category (HIV status and ART status)?'),
        choices=YES_NO,
        max_length=3)

    child_dob = models.DateField(verbose_name='Child date of birth')

    child_age = models.IntegerField()

    child_is_of_age = models.CharField(
        verbose_name='Child is age 23-28 months',
        choices=YES_NO,
        max_length=3)

    child_hiv_neg = models.CharField(
        verbose_name='Child is documented to have negative HIV test after 18 months of age',
        choices=YES_NO,
        max_length=3)

    child_test_date = models.DateField(verbose_name='Date of negative test')

    child_test_type = models.CharField(
        verbose_name='Type of negative test',
        choices=TEST_TYPES,
        max_length=15)

    child_test_type_other = OtherCharField()

    team_performed_test = models.CharField(
        verbose_name='Test performed by Motheo study team?',
        choices=YES_NO,
        max_length=3)

    add_reasons_ineligible = models.CharField(
        verbose_name=('Are there any additional reason(s) why the mother-infant'
                      ' pair was not enrolled in this study?'),
        choices=YES_NO,
        max_length=3)

    specify_reasons = models.TextField(
        verbose_name='if yes, specify: ',
        max_length=500)

    consent_discussed = models.CharField(
        verbose_name='Study overview discussed with participant and all questions answered?',
        choices=YES_NO,
        max_length=3)

    consent_review = models.CharField(
        verbose_name='Participant reviewed the informed consent and all questions answered?',
        choices=YES_NO,
        max_length=3)

    consent_signed = models.CharField(
        verbose_name='Participant signed the consent form?',
        choices=YES_NO,
        max_length=3)

    consent_samples = models.CharField(
        verbose_name='Did the participant consent for having samples used for future research?',
        choices=YES_NO,
        max_length=3)

    consent_copy = models.CharField(
        verbose_name='Participant given a copy of the consent form?',
        choices=YES_NO,
        max_length=3)

    consent_received = models.CharField(
        verbose_name='Consent received by study coordinator for filling or scanned?',
        choices=YES_NO,
        max_length=3)

    class Meta:
        abstract = True
