from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .call_models import Call
from ..classes import EmailSchedule


@receiver(post_save, weak=False, sender=Call,
          dispatch_uid="call_on_post_save")
def call_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        if created:
            subject_identifier = instance.subject_identifier
            subject = f'Motheo call reminder for participant: {subject_identifier}'

            message_data = ('Hi, \n \n'
                            f'Please be reminded the call to participant '
                            f'{instance.first_name} subject identifier {subject_identifier}'
                            'is due today. \n \n'
                            'Good day :).')

            users = User.objects.filter(groups__name__in=['RA'])
            to_emails = [user.email for user in users]

            schedule_datetime = instance.scheduled
            EmailSchedule().schedule_email(
                subject, message_data, to_emails, schedule_datetime)
