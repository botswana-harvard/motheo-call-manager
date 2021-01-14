import configparser
from django.conf import settings

from .redcap_request import RedcapRequest


class ImportRecordInstance(object):

    def __init__(self, name=""):
        """
        @param url: str - API URL to your REDCap server
        @param token: API token to your project
        @param name:  name for project (optional)
        """

        self.url, self.token = self.configuration()
        self.name = name
        self.metadata = None
        self.redcap_version = None
        self.field_names = None

    def configuration(self):
        configs = list()
        config = configparser.ConfigParser()

        settings_dict = settings.REDCAP_CONFIGURATION
        config_file = settings_dict['OPTIONS'].get('read_default_file')
        config.read(config_file)
        if config_file:
            configs.append(config['read']['api_url'])
            configs.append(config['read']['api_token'])
        return configs

    def _call_api(self, payload, r_type, **kwargs):
        rcr = RedcapRequest(self.url, payload, r_type)
        return rcr.execute(**kwargs)

    def __basepl(self, content, rec_type='flat', format_key='json'):
        """Return a dictionary which can be used as is or added to for
        payloads"""
        payload_dict = {'token': self.token,
                        'content': content,
                        'format': format_key}
        if content not in ['metapayload_dictata', 'file']:
            payload_dict['type'] = rec_type
        return payload_dict

    def export_records(
            self, records=None, fields=None, forms=None, events=None,
            raw_or_label='raw', format_key='json', export_survey_fields=False,
            export_checkbox_labels=False):
        """
        Export data from the REDCap project.

        @param  records : array of record names for specific records to export.
        @param  fields : array of field names for specific fields to pull
        @param  forms : array of form names to export.
        @param  events : an array of unique event names from which to export records
                :note: this only applies to longitudinal projects
        @param  raw_or_label : (``'raw'``), ``'label'``, ``'both'``
                export the raw coded values or labels for the options of
                multiple choice fields, or both
        @param  format_key : (``'json'``), ``'csv'``, ``'xml'``, ``'df'``
                Format of returned data. ``'json'`` returns json-decoded
                objects while ``'csv'`` and ``'xml'`` return other formats.
        @param  export_survey_fields : (``False``), True
                specifies whether or not to export the survey identifier field
                (e.g., "redcap_survey_identifier") or survey timestamp fields
                (e.g., form_name+"_timestamp") when surveys are utilized in the project.

            :note: This flag is only viable if the user whose token is
                being used to make the API request is *not* in a data
                access group. If the user is in a group, then this flag
                will revert to its default value.

        @param  export_checkbox_labels : (``False``), ``True``
                specify whether to export checkbox values as their label on
                export.
        @param  filter_logic : string specify the filter logic to be sent to the API.
        @param  date_begin : datetime for the dateRangeStart filtering of the API
        @param  date_end : datetime for the dateRangeEnd filtering snet to the API
        -------
        @return: response (json)
        """

        ret_format = format_key

        payload = self.__basepl('record', format_key=ret_format)
        fields = fields
        keys_to_add = (
            records,
            fields,
            forms,
            events,
            raw_or_label,
            export_survey_fields,
            export_checkbox_labels,
        )

        str_keys = (
            'records',
            'fields',
            'forms',
            'events',
            'rawOrLabel',
            'exportSurveyFields',
            'exportCheckboxLabel',
        )

        for key, data in zip(str_keys, keys_to_add):
            if data:
                if key in ('fields', 'records', 'forms', 'events'):
                    for i, value in enumerate(data):
                        payload['{}[{}]'.format(key, i)] = value
                else:
                    payload[key] = data

        response, _ = self._call_api(payload, 'exp_record')
        if format_key in ('json', 'csv', 'xml'):
            return response
        else:
            raise ValueError(('Unsupported format: \'{}\'').format(format))

    def backfill_fields(self, fields, forms):
        """
        Properly back-fill fields to explicitly request specific keys.

        @param fields: requested fields
        @param forms: requested forms

        """
        if forms and not fields:
            new_fields = [self.def_field]
        elif fields and self.def_field not in fields:
            new_fields = list(fields)
            if self.def_field not in fields:
                new_fields.append(self.def_field)
        elif not fields:
            new_fields = self.field_names
        else:
            new_fields = list(fields)
        return new_fields
