import configparser
import datetime
from dateutil.relativedelta import relativedelta
import os

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...classes import ImportRecordInstance
from ...constants import CONTACTED
from ...models import SubjectLocator, CallLogEntry
from ...serializers import SubjectLocatorSerializer
from edc_call_manager.constants import NO_CONTACT
from django.conf import settings


class TriggerView(APIView):

    def post(self, request, *args, **kwargs):
        redcap_config = configparser.ConfigParser()
        redcap_config.read(os.path.join(settings.ETC_DIR, 'motheo_call_manager.ini'))

        record = request.POST.get('record', None)
        username = request.POST.get('username', None)
        event_name = request.POST.get('redcap_event_name', None)

        CallLogEntry.objects.create(
            subject_identifier=record,
            user_created=username,
            event_name=event_name
        )

        return Response(status=status.HTTP_200_OK)
