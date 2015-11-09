""" HTTP Status headers """

class HTTPStatus(Exception):

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

    def __init__(self, message=None):
        super(HTTPError, self).__init__(self, message)
        self.message = message


class HTTPRedirect(HTTPError):
    """Abstract redirect.
    
    Args:
        url (str):
        absolute (bool):
    
    Note:
        `url` is joined with the base URL so that things like `redirect("about") will work properly.

    """

    status = None

    def __init__(self, path, url):
        new_path = urlparse.urljoin(path, url)
        self.headers = {
            'Content-Type': 'text/html',
            'Location': new_path
        }
        HTTPError.__init__(self)


class Redirect(HTTPRedirect):
    """A `301 Moved Permanently` redirect."""

    status = '301 Moved Permanently'


class Found(Redirect):
    """A `302 Found` redirect."""

    status = '302 Found'


class SeeOther(Redirect):
    """A `303 See Other` redirect."""

    status = '303 See Other'
    

class NotModified(HTTPError):
    """A `304 Not Modified` status."""

    status = '304 Not Modified'


class TempRedirect(Redirect):
    """A `307 Temporary Redirect` redirect."""

    status = '307 Temporary Redirect'


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
        super(NotFound, self).__init__(self.message.format(path))


class NoMethod(HTTPError):
    """A `405 Method Not Allowed` error."""

    def __init__(self, app):
        status = '405 Method Not Allowed'
        headers = {'Content-Type': 'text/html'}
        methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE']
        if cls:
            methods = [method for method in methods if hasattr(cls, method)]
        headers['Allow'] = ', '.join(methods)
        super(NoMethod, self).__init__(status, headers)
        

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


CODE_TO_STATS_MAP = {200: OK,
                     201: Created,
                     202: Accepted,
                     301: Redirect,
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
