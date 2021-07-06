import pytz
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import make_aware
from edc_base.utils import get_utcnow

from .call_models import Call, LogEntry
from .home_visit import HomeVisit
from ..classes import EmailSchedule


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
            schedule_datetime = make_aware(schedule_datetime, pytz.timezone(settings.TIME_ZONE))
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
