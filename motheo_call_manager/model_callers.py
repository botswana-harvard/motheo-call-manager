from edc_call_manager.constants import DAILY
from edc_call_manager.decorators import register
from edc_call_manager.model_caller import ModelCaller

from .models import SubjectLocator, SubjectOffStudy


@register(SubjectLocator, SubjectOffStudy)
class FollowUpModelCaller(ModelCaller):
    locator_model = SubjectLocator
    subject_model = SubjectLocator
    interval = DAILY
