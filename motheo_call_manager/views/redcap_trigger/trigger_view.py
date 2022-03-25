import configparser
import datetime
import threading
from time import sleep
from dateutil.relativedelta import relativedelta
import os
import pytz


import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...constants import CONTACTED
from ...serializers import SubjectLocatorSerializer
from edc_call_manager.constants import NO_CONTACT
from django.conf import settings
from ...cron.email_sender_cron import EmailSenderCron


class EmailSchedularHelper(threading.Thread):
    def __init__(self, token, record, event_name):
        self._token = token
        self._record = record
        self._event_name = event_name
        threading.Thread.__init__(self)

    def run(self):
        self._schedule_email()

    def _message(self, subject_identitfier, date: datetime.datetime):
        return f"""\
            Good day 

            {subject_identitfier} call is due tomorrow ({date.date()}), please take note.

            Best regards

            Motheo Bot
            """

    def _schedule_email(self):

        sleep(3) # delay to wait for redcap to save form

        data = {
            'token': self._token,
            'content': 'record',
            'format': 'json',
            'type': 'flat',
            'csvDelimiter': '',
            'records[0]': self._record,
            'fields[0]': 'call_attempt_dt',
            'fields[1]': 'call_outcome',
            'forms[0]': 'call_log_entry',
            'events[0]': self._event_name,
            'rawOrLabel': 'raw',
            'rawOrLabelHeaders': 'raw',
            'exportCheckboxLabel': 'false',
            'exportSurveyFields': 'false',
            'exportDataAccessGroups': 'false',
            'returnFormat': 'json'
        } # data used to fetch records

        response = requests.post(settings.REDCAP_API_URL, data=data)

        if response.status_code == status.HTTP_200_OK:
            json = response.json()[0]
            call_outcome = json['call_outcome']
            call_attempt_dt = json['call_attempt_dt'][:-6]
            subject_identifier = json['call_subid']

            if json['call_outcome'] == "0": 
                # if outcome is succesful its eq to 0

                next_call = None

                if settings.DEBUG:
                    next_call = datetime.datetime.now() + relativedelta(seconds=3)
                else:
                    next_call = datetime.datetime.fromisoformat(
                        call_attempt_dt) + relativedelta(months=3)

                # schedule a crone job
                EmailSenderCron(
                    token=self._token,
                    next_call_dt=next_call,
                    title="Follow Up",
                    message=self._message(subject_identifier)
                ).schedule_mail()


class TriggerView(APIView):

    def post(self, request, *args, **kwargs):
        redcap_config = configparser.ConfigParser()
        redcap_config.read(os.path.join(
            settings.ETC_DIR, 'motheo_call_manager.ini'))

        record = request.POST.get('record', None)
        event_name = request.POST.get('redcap_event_name', None)

        thread = EmailSchedularHelper(
            token=redcap_config['redcap']['token'],
            record=record,
            event_name=event_name
        )

        thread.setDaemon(True)

        thread.start()

        return Response(status=status.HTTP_200_OK)
