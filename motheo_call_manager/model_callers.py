from edc_call_manager.constants import DAILY
from edc_call_manager.decorators import register
from edc_call_manager.model_caller import ModelCaller

from .models import SubjectLocator, SubjectOffStudy, Call, Log, LogEntry


@register(SubjectLocator, SubjectOffStudy)
class FollowUpModelCaller(ModelCaller):
    call_model = Call
    log_model = Log
    log_entry_model = LogEntry
    locator_model = SubjectLocator
    subject_model = SubjectLocator
    interval = DAILY
