import configparser
from datetime import date, timedelta
import email
import imp
import os
from urllib import response
from django.conf import settings
import requests
from rest_framework import status
from django_q.tasks import schedule, async_task
from django_q.models import Schedule


class EmailSenderCron:

    def __init__(self, token,title, message, next_call_dt):
        self._data = {
            'token': token,
            'content': 'user',
            'format': 'json',
            'returnFormat': 'json'
        }
        self._message = message
        self._title = title

        self._emails = self._collect_emails()
        self._next_run = next_call_dt - timedelta(days=1)
    
    def _collect_emails(self):

        response = requests.post(
            'https://redcap-dev.bhp.org.bw/api/', data=self._data)

        emails = list()
            
        if response.status_code == status.HTTP_200_OK:
            json = response.json()
            for j in json:
                emails.append(j['email'])

        return emails

    def _send_email_cron(self):
        msg = 'Welcome to our website'

        # and this follow up email in one hour
        msg = 'Here are some tips to get you started...'

        schedule('django.core.mail.send_mail',
                self._title, self._message,
                 'mail.bhp.org.bw',
                self._emails,
                schedule_type=Schedule.ONCE,
                next_run= self._next_run)

    def schedule_mail(self):
        self._send_email_cron()

