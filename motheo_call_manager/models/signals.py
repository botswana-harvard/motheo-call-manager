import configparser
import os
from time import sleep
from datetime import datetime, time
from threading import Thread

import pytz
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import make_aware
from edc_call_manager.constants import NO_CONTACT
from rest_framework import status

from .call_models import *
from .home_visit import HomeVisit
from ..classes import EmailSchedule
from ..constants import CONTACTED


def delayed_save(instance: CallLogEntry):
    sleep(5)
    redcap_config = configparser.ConfigParser()
    redcap_config.read(os.path.join(
        settings.ETC_DIR, 'motheo_call_manager.ini'))
    data = {
        'token': redcap_config['redcap']['token'],
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'records[0]': instance.subject_identifier,
        'fields[0]': 'call_attempt_dt',
        'fields[1]': 'call_outcome',
        'forms[0]': 'call_log_entry',
        'events[0]': instance.event_name,
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }

    response = requests.post(settings.REDCAP_API_URL, data=data)
    if response.status_code == status.HTTP_200_OK:
        json = response.json()[0]
        print(json)

        call_outcome = CONTACTED if json['call_outcome'] == '0' else NO_CONTACT
        call_attempt_dt = json['call_attempt_dt'][:-6]
        subject_identifier = json['call_subid']

        if call_outcome == CONTACTED:
            import pdb
            pdb.set_trace()
            instance.subject_identifier = subject_identifier
            instance.call_outcome = call_outcome
            instance.call_attempt_dt = call_attempt_dt
            instance.next_call = datetime.fromisoformat(
                call_attempt_dt) + relativedelta(months=3)

            instance.save()
        else:
            instance.delete()
    else:
        pass


@receiver(post_save, weak=False, sender=CallLogEntry,
          dispatch_uid="call_log_entry_post_save")
def call_log_entry_post_save(sender, instance, raw, created, **kwargs):

    if instance and not instance.next_call:
        thread = Thread(name="delayed_save",
                        target=delayed_save, args=(instance,))
        thread.setDaemon(True)
        thread.start()


@receiver(post_save, weak=False, sender=Call,
          dispatch_uid="call_on_post_save")
def call_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        if created and instance.scheduled != get_utcnow().date():
            subject_identifier = instance.subject_identifier
            subject = f'Motheo call reminder for participant: {subject_identifier}'

            message_data = ('Hi, \n \n'
                            f'Please be reminded the call to participant '
                            f'{instance.first_name} subject identifier '
                            f'{subject_identifier} is due on the '
                            f'{instance.scheduled}. \n \n Good day :).')

            users = User.objects.filter(groups__name__in=['RA', 'Research Nurse',
                                                          'Study coordinator'])
            to_emails = [user.email for user in users]

            schedule_date = instance.scheduled - relativedelta(days=1)
            schedule_time = time(hour=8, minute=30, second=0)
            schedule_datetime = datetime.combine(schedule_date, schedule_time)
            schedule_datetime = make_aware(
                schedule_datetime, pytz.timezone(settings.TIME_ZONE))
            EmailSchedule().schedule_email(
                subject, message_data, to_emails, schedule_datetime)


@receiver(post_save, weak=False, sender=LogEntry,
          dispatch_uid="log_entry_on_post_save")
def log_entry_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        log_entries = LogEntry.objects.filter(
            log=instance.log,
            call_datetime__month=instance.call_datetime.month).order_by(
            '-call_datetime')
        if len(log_entries) > 4:
            latest_entries = log_entries[:5]
            if all(entry.contact_type == 'no_contact' for entry in latest_entries):
                try:
                    HomeVisit.objects.get(
                        subject_identifier=instance.log.call.subject_identifier,
                        scheduled_date__month=instance.call_datetime.month)
                except HomeVisit.DoesNotExist:
                    HomeVisit.objects.create(
                        subject_identifier=instance.log.call.subject_identifier,
                        scheduled_date=instance.call_datetime.date(),
                        user_created=instance.user_created)
