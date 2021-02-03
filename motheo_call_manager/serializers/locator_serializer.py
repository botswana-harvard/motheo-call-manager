from rest_framework import serializers, fields
from ..models import SubjectLocator


class SubjectLocatorSerializer(serializers.ModelSerializer):

    loc_date = fields.DateField(input_formats=['%Y-%m-%d'])

    date_followup = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = SubjectLocator
        fields = ('subject_identifier',
                  'loc_admin',
                  'loc_date',
                  'first_name',
                  'last_name',
                  'initials',
                  'subject_cell',
                  'may_call',
                  'subject_cell_alt',
                  'may_call_alt',
                  'subject_phone',
                  'may_call_tel',
                  'loc_email',
                  'may_contact_email',
                  'loc_village',
                  'loc_address',
                  'may_visit_home',
                  'idcc_clinic',
                  'may_contact_idcc',
                  'loc_workplace',
                  'loc_workphone',
                  'may_contact_work',
                  'loc_kincontact',
                  'may_contact_kin',
                  'date_followup',
                  'review_locator', )

    def create(self, validated_data):
        """
        Create and return a new `SubjectLocator` instance, given the validated data.
        """
        return SubjectLocator.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `SubjectLocator` instance, given the validated data.
        """
        subject_identifier = validated_data.get(
            'subject_identifier', instance.subject_identifier)
        SubjectLocator.objects.filter(
            subject_identifier=subject_identifier).update(**validated_data)
        return instance
