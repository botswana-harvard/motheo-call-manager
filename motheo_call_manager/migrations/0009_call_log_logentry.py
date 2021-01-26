# Generated by Django 3.1.3 on 2021-01-22 10:25

import _socket
import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_crypto_fields.fields.encrypted_text_field
import django_crypto_fields.fields.firstname_field
import django_revision.revision_field
import edc_base.model_fields.custom_fields
import edc_base.model_fields.hostname_modification_field
import edc_base.model_fields.userfield
import edc_base.model_fields.uuid_auto_field
import edc_base.model_validators.date
import edc_base.utils
import edc_call_manager.managers
import edc_protocol.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('motheo_call_manager', '0008_auto_20210114_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_base.model_fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_base.model_fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('subject_identifier', models.CharField(max_length=50)),
                ('label', models.CharField(max_length=50)),
                ('scheduled', models.DateField(default=datetime.date.today)),
                ('repeats', models.BooleanField(default=False)),
                ('call_datetime', models.DateTimeField(editable=False, help_text='last call datetime updated by call log entry', null=True)),
                ('first_name', django_crypto_fields.fields.firstname_field.FirstnameField(blank=True, editable=False, help_text=' (Encryption: RSA local)', max_length=71, null=True, verbose_name='First name')),
                ('initials', models.CharField(editable=False, max_length=3, null=True, verbose_name='Initials')),
                ('consent_datetime', models.DateTimeField(help_text='From Subject Consent.', null=True, validators=[edc_protocol.validators.datetime_not_before_study_start, edc_base.model_validators.date.datetime_not_future], verbose_name='Consent date and time')),
                ('call_attempts', models.IntegerField(default=0)),
                ('call_outcome', models.TextField(max_length=150, null=True)),
                ('call_status', models.CharField(choices=[('NEW', 'New'), ('open', 'Open'), ('closed', 'Closed')], default='NEW', max_length=15)),
                ('auto_closed', models.BooleanField(default=False, editable=False, help_text='If True call status was changed to CLOSED by EDC.')),
                ('site', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='sites.site')),
            ],
            options={
                'abstract': False,
                'unique_together': {('subject_identifier', 'label', 'scheduled')},
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_base.model_fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_base.model_fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('log_datetime', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('locator_information', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text='This information has been imported from the previous locator. You may update as required. (Encryption: AES local)', max_length=71, null=True)),
                ('contact_notes', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True)),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motheo_call_manager.call')),
            ],
            options={
                'abstract': False,
                'unique_together': {('log_datetime', 'call')},
            },
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_base.model_fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_base.model_fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('call_reason', models.CharField(choices=[('schedule_appt', 'Schedule an appointment'), ('reminder', 'Remind participant of scheduled appointment'), ('missed_appt', 'Follow-up with participant on missed appointment')], max_length=25, verbose_name='Reason for this call')),
                ('call_datetime', models.DateTimeField(verbose_name='Date of this call')),
                ('contact_type', models.CharField(choices=[('direct', 'Direct contact with participant'), ('indirect', 'Contact with person other than participant'), ('no_contact', 'No contact made')], help_text='If no contact made. STOP. Save form.', max_length=15)),
                ('survival_status', models.CharField(choices=[('alive', 'Alive'), ('dead', 'Deceased'), ('unknown', 'Unknown')], default='alive', max_length=10, null=True, verbose_name='Survival status of the participant')),
                ('time_of_week', models.CharField(blank=True, choices=[('weekdays', 'Weekdays'), ('weekends', 'Weekends'), ('anytime', 'Anytime')], max_length=25, null=True, verbose_name='Time of week when participant will be available')),
                ('time_of_day', models.CharField(blank=True, choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening'), ('anytime', 'Anytime')], max_length=25, null=True, verbose_name='Time of day when participant will be available')),
                ('appt', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=7, null=True, verbose_name='Is the participant willing to schedule an appointment')),
                ('appt_reason_unwilling', models.CharField(blank=True, choices=[('not_interested', 'Not interested in participating'), ('busy', 'Busy during the suggested times'), ('away', 'Out of town during the suggested times'), ('unavailable', 'Not available during the suggested times'), ('DWTA', 'Prefer not to say why I am unwilling.'), ('OTHER', 'Other reason ...')], max_length=25, null=True, verbose_name='What is the reason the participant is unwilling to schedule an appointment')),
                ('appt_reason_unwilling_other', models.CharField(blank=True, max_length=50, null=True, verbose_name='Other reason, please specify ...')),
                ('appt_date', models.DateField(blank=True, help_text='This can only come from the participant.', null=True, validators=[edc_base.model_validators.date.date_is_future], verbose_name='Appointment Date')),
                ('appt_grading', models.CharField(blank=True, choices=[('firm', 'Firm appointment'), ('weak', 'Possible appointment'), ('guess', 'Estimated by RA')], max_length=25, null=True, verbose_name='Is this appointment...')),
                ('appt_location', models.CharField(blank=True, choices=[('home', 'At home'), ('work', 'At work'), ('telephone', 'By telephone'), ('clinic', 'At clinic'), ('OTHER', 'Other location')], max_length=50, null=True, verbose_name='Appointment location')),
                ('appt_location_other', edc_base.model_fields.custom_fields.OtherCharField(blank=True, max_length=50, null=True, verbose_name='Other location, please specify ...')),
                ('delivered', models.BooleanField(default=False, editable=False, null=True)),
                ('may_call', models.CharField(blank=True, choices=[('Yes', 'Yes, we may continue to contact the participant.'), ('No', 'No, participant has asked NOT to be contacted again.')], default='Yes', max_length=10, null=True, verbose_name='May we continue to contact the participant?')),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motheo_call_manager.log')),
            ],
            options={
                'abstract': False,
                'unique_together': {('call_datetime', 'log')},
            },
            managers=[
                ('objects', edc_call_manager.managers.LogEntryManager()),
            ],
        ),
    ]
