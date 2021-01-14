import json
from requests import Session, RequestException

_session = Session()


class RedcapAPIError(Exception):
    pass


class RedcapRequest(object):

    def __init__(self, url, payload, query_type, session=_session):
        """
        @param url : REDCap API URL
        @param payload : {key,values} corresponding to the REDCap API
        """
        self.url = url
        self.payload = payload
        self.session = session
        self.type = query_type

        if query_type:
            self.validate_export_records_fields()

        format_key = 'returnFormat' if 'returnFormat' in payload else 'format'
        self.format = payload[format_key]

    def execute(self, **kwargs):
        """
        Execute the API request and return dataParameters
        @param kwargs:
        @return: response => data object from JSON decoding process
                            if format=='json', else return raw string
                            (i.e format=='csv' | 'xml')
        """
        response = self.session.post(self.url, data=self.payload, **kwargs)
        # Raise if we need to
        self.raise_for_status(response)
        content = self.get_content(response)
        return content, response.headers

    def validate_export_records_fields(self):
        """Checks that at least required export records fields exist"""

        required = ['token', 'content']
        valid_data = {
            'exp_record': (
                ['type', 'format'],
                'record',
                'Exporting record but content is not record',
            ),
        }

        extra, req_content, error_msg = valid_data[self.type]

        required.extend(extra)

        required = set(required)
        pl_keys = set(self.payload.keys())

        if not set(required) <= pl_keys:

            not_pre = required.difference(pl_keys)
            raise RedcapAPIError('Required keys: %s' % ', '.join(not_pre))

        try:
            if self.payload['content'] != req_content:
                raise RedcapAPIError(error_msg)
        except KeyError as key_fail:
            raise RedcapAPIError('content not in payload') from key_fail

    def get_content(self, resp):
        """Extract content from a returned response"""

        if self.format == 'json':
            content = {}
            try:
                content = json.loads(resp.text, strict=False)
            except ValueError as e:
                if not self.expect_empty_json():
                    raise ValueError(e) from e
            finally:
                return content
        return resp.text

    def expect_empty_json(self):
        """Del and import file responses are known to send empty responses"""
        return self.type in ('imp_file', 'del_file')

    def raise_for_status(self, resp):
        if 500 <= resp.status_code < 600:
            raise RequestException(resp.content)

        if resp.status_code == 400 and self.type == 'exp_record':
            raise RequestException(resp.content)
