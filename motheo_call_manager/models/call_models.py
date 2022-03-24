from operator import mod
from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from ..choices import CALL_OUTCOME
from dateutil.relativedelta import relativedelta
from edc_call_manager.model_mixins import (
    CallModelMixin, LogModelMixin, LogEntryModelMixin)


class Call(CallModelMixin, BaseUuidModel):
    scheduled = models.DateTimeField(
        default=get_utcnow)

    class Meta(CallModelMixin.Meta):
        app_label = 'motheo_call_manager'


class Log(LogModelMixin, BaseUuidModel):
    call = models.ForeignKey(Call, on_delete=models.PROTECT)

    class Meta(LogModelMixin.Meta):
        app_label = 'motheo_call_manager'


class LogEntry(LogEntryModelMixin, BaseUuidModel):
    log = models.ForeignKey(Log, on_delete=models.PROTECT)

    class Meta(LogEntryModelMixin.Meta):
        app_label = 'motheo_call_manager'


# class CallLogEntry(BaseUuidModel):
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.CharField(max_length=20)
#     instrument = models.CharField(max_length=20)
#     event_name = models.CharField(max_length=30)
#     subject_identifier = models.CharField(max_length=16)
#     call_outcome = models.CharField(max_length=20, choices=CALL_OUTCOME)
#     next_call = models.DateField(blank=True, null=True)


class CallLogEntry(BaseUuidModel):
    '''
    One to one map of some of the fields from redcap
    witout compromising privacy by storing phone numbers
    '''

    subject_identifier = models.CharField(max_length=20)
    event_name = models.CharField(max_length=20)
    call_attempt_dt = models.DateField(null=True, blank=True)
    call_outcome = models.CharField(max_length=20, choices=CALL_OUTCOME, null=True, blank=True)
    next_call = models.DateField(null=True, blank=True)
