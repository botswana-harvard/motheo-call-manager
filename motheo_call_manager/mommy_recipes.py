from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from faker import Faker
from model_mommy.recipe import Recipe

from .models import SubjectLocator

fake = Faker()

subjectlocator = Recipe(
    SubjectLocator,
    loc_date=get_utcnow(),
    first_name='Jane',
    last_name='Doe',
    initials='JD',
    may_call=YES,
    may_call_alt=YES,
    may_call_tel=YES,
    date_followup=(get_utcnow() + relativedelta(months=1)).date())
