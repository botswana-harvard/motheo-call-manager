from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow

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
