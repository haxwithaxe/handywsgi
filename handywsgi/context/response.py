
import io

import handywsgi.buffer
import handywsgi.status
import handywsgi.headers
import handywsgi.content_type


class Response:
    """ Encapsulation of response data to be sent from the server.

    Attributes:
        headers (handywsgi.headers.Headers): HTTP headers.
        output (Content): A buffer for output content.
        content_type (headers.Header): Content-Type header.
        status (status.HTTPStatus): HTTP status object.

    Args:
        start_response (callable): WSGI start_response function.
        status_header (status.HTTPStatus): Defaults to ``handywsgi.status.OK``.
        content_type (headers.Header): Defaults to ``handywsgi.content_type.HTML_UTF8``.

    """

    def __init__(self,
                 start_response,
                 status_header=handywsgi.status.OK,
                 content_type=handywsgi.content_type.HTML_UTF8):
        self._start_response = start_response
        self._status = status_header
        self._content_type = content_type
        self.headers = handywsgi.headers.Headers()
        self.output = OutputContent()

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, spec):
        self._content_type = handywsgi.headers.Header(
                'Content-Type',
                '{mime};charset={encoding}'.format(**spec),
                unique=True)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, code):
        if isinstance(code, handywsgi.status.HTTPStatus):
            self._status = code
        else:
            self._status = handywsgi.status.from_code(code)

    def start(self):
        self._start_response(self.status, self.headers)


class OutputContent(handywsgi.buffer.IOBuffer):

    def __init__(self, filename=None):
        buffer_class = None
        if filename:
            buffer_class = handywsgi.buffer.file_io(filename)
        super().__init__(buffer_class=buffer_class)
