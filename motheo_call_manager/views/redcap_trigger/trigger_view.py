from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...classes import ImportRecordInstance
from ...models import SubjectLocator
from ...serializers import SubjectLocatorSerializer


class TriggerView(APIView):

    import_record_cls = ImportRecordInstance

    def post(self, request, *args, **kwargs):
        data_dict = {}

        if request.method == 'POST':
            data_dict = request.POST.dict()
            form_name = data_dict.get('instrument')
            if form_name == 'locator_form':
                rs = self.import_record_cls().export_records(
                    records=[data_dict.get('record'), ], forms=[form_name, ],
                    raw_or_label='label', export_checkbox_labels=True)

                identifier = data_dict.get('record')

                locator_dict = {'subject_identifier': identifier}
                rs[0].pop('locator_form_complete', None)
                locator_dict.update(rs[0])

                if self.locator_exists(subject_identifier=identifier):
                    return self.populate_locator(locator_dict, update=True)
                return self.populate_locator(locator_dict)
            return Response({})

    def populate_locator(self, locator_data, update=False):
        if not update:
            import pdb; pdb.set_trace()
            locator_serializer = SubjectLocatorSerializer(data=locator_data)
            if locator_serializer.is_valid():
                locator_serializer.save()
                return Response(locator_serializer.data, status=status.HTTP_201_CREATED)
            return Response(locator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            subject_identifier = locator_data.get('subject_identifier')
            locator = SubjectLocator.objects.get(subject_identifier=subject_identifier)
            locator_serializer = SubjectLocatorSerializer(locator, data=locator_data) 
            if locator_serializer.is_valid():
                locator_serializer.save()
                return Response(locator_serializer.data)
            return Response(locator_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def locator_exists(self, subject_identifier=None):
        if subject_identifier:
            try:
                SubjectLocator.objects.get(subject_identifier=subject_identifier)
            except SubjectLocator.DoesNotExist:
                return False
            else:
                return True
