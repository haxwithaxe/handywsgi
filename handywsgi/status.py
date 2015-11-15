""" HTTP Status headers """


import urllib

from . import HTTP_REQUEST_METHODS

class HTTPStatus(Exception):
    """ HTTP Status code base class.

    Attributes:
        status (str): The full HTTP Status code string.
        message (str): The message to display in the stacktrace
        headers (list): A list of header.Header to add to the response.

    """

    status = None
    message = None
    headers = []


class OK(HTTPStatus):

    status = '200 OK'


class Created(HTTPStatus):

    status = '201 Created'


class Accepted(HTTPStatus):

    status = '202 Accepted'


class HTTPError(HTTPStatus):
    """ HTTP Error stats code base class. """

    def __init__(self, message=None):
        super().__init__(message)
        self.message = message


class NotModified(HTTPError):
    """A `304 Not Modified` status."""

    status = '304 Not Modified'


class BadRequest(HTTPError):
    """`400 Bad Request` error."""

    message = 'bad request'
    status = '400 Bad Request'


class Unauthorized(HTTPError):
    """`401 Unauthorized` error."""

    message = 'unauthorized'
    status = '401 Unauthorized'


class Forbidden(HTTPError):
    """`403 Forbidden` error."""

    message = 'forbidden'
    status = '403 Forbidden'


class NotFound(HTTPError):
    """`404 Not Found` error."""

    message = '{} not found'
    status = '404 Not Found'

    def __init__(self, path):
        super().__init__(message=self.message.format(path))


class NoMethod(HTTPError):
    """A `405 Method Not Allowed` error."""

    status = '405 Method Not Allowed'

    def __init__(self, app):
        super().__init__()
        self.headers = {'Content-Type': 'text/html'}
        methods = HTTP_REQUEST_METHODS
        if app:
            methods = [method for method in methods if hasattr(app, method)]
        self.headers['Allow'] = ', '.join(methods)


class NotAcceptable(HTTPError):
    """`406 Not Acceptable` error."""

    message = 'not acceptable'
    status = '406 Not Acceptable'


class Conflict(HTTPError):
    """`409 Conflict` error."""

    message = 'conflict'
    status = '409 Conflict'



class Gone(HTTPError):
    """`410 Gone` error."""

    message = 'gone'
    status = '410 Gone'


class PreconditionFailed(HTTPError):
    """`412 Precondition Failed` error."""

    message = 'precondition failed'
    status = '412 Precondition Failed'


class UnsupportedMediaType(HTTPError):
    """`415 Unsupported Media Type` error."""

    message = 'unsupported media type'
    status = '415 Unsupported Media Type'


class InternalError(HTTPError):
    """`500 Internal Server Error`."""

    message = 'internal server error'
    status = '500 Internal Server Error'


class HTTPRedirect(HTTPError):
    """Abstract redirect.

    Args:
        url (str):
        absolute (bool):

    Note:
        `url` is joined with the base URL so that things like `redirect("about") will work properly.

    """

    def __init__(self, path, url):
        super().__init__()
        new_path = urllib2.parse.urlparse.urljoin(path, url)
        self.headers = {
            'Content-Type': 'text/html',
            'Location': new_path
        }


class PermanentRedirect(HTTPRedirect):
    """A `301 Moved Permanently` redirect."""

    status = '301 Moved Permanently'


class Found(HTTPRedirect):
    """A `302 Found` redirect."""

    status = '302 Found'


class SeeOther(HTTPRedirect):
    """A `303 See Other` redirect."""

    status = '303 See Other'


class TempRedirect(HTTPRedirect):
    """A `307 Temporary Redirect` redirect."""

    status = '307 Temporary Redirect'




CODE_TO_STATS_MAP = {200: OK,
                     201: Created,
                     202: Accepted,
                     301: PermanentRedirect,
                     302: Found,
                     303: SeeOther,
                     304: NotModified,
                     307: TempRedirect,
                     400: BadRequest,
                     401: Unauthorized,
                     403: Forbidden,
                     404: NotFound,
                     405: NoMethod,
                     406: NotAcceptable,
                     409: Conflict,
                     410: Gone,
                     412: PreconditionFailed,
                     415: UnsupportedMediaType,
                     500: InternalError}


def from_code(code):
    status = CODE_TO_STATS_MAP.get(code)
    if not status:
        raise ValueError('%s is not a supported HTTP status code' % code)
    return status
