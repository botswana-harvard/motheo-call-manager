from django_q.tasks import schedule


class EmailSchedule:

    def schedule_email(self, subject=None, message_data=None, to_emails=[],
                       schedule_datetime=None):

        from_email = 'adiphoko@bhp.org.bw'

        # Schedule an email reminder
        schedule(
            'django.core.mail.send_mail',
            subject,
            message_data,
            from_email,
            to_emails,
            schedule_type='O',
            next_run=schedule_datetime)
