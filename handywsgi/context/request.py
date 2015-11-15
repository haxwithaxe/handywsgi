
import cgi
import urllib


class Request:
    """ Encapsulation of the data in the request to the server.

    Attributes:

        environment (dict): os.envron
        wsgi (WSGIData): PEP-3333 wsgi environ
        netloc (str): Server name (and port for nonstandard ports).
        url (str): The full request URL (cleaned up).
        content (object): CONTENT_* CGI variables.
        http (object): HTTP_* CGI variables.
        query (object): QUERY_* CGI variables.
        client (object): CLIENT_* CGI variables.
        script (object): SCRIPT_*, PATH_*, and REQUEST_* CGI variables.
        server (object): SERVER_* CGI variables.

    """

    def __init__(self, environment):
        self.environment = environment.copy()
        self.wsgi = WSGIData(environment.copy())
        self._get_request_parts(environment.copy())
        if self.server.port not in (None, '', 80, 443):
            self.netloc = '{}:{}'.format(self.server.name, self.server.port)
        else:
            self.netloc = self.server.name
        self.url = urllib.parse.urlunparse(
            (self.wsgi.url_scheme, self.netloc, self.query.path, self.query.param, '', '')
            )

    def _get_request_parts(self, environment):
        """ Build up the object model of the incoming data. """
        class Content:
            length = environment.get('CONTENT_LENGTH')
            mime = environment.get('CONTENT_TYPE')
        self.content = Content()

        class HTTP:
            accept = environment.get('HTTP_ACCEPT')
            accept_encoding = environment.get('HTTP_ACCEPT_ENCODING')
            accept_language = environment.get('HTTP_ACCEPT_LANGUAGE')
            cache_control = environment.get('HTTP_CACHE_CONTROL')
            connection = environment.get('HTTP_CONNECTION')
            hostname = environment.get('HTTP_HOST')
            user_agent = environment.get('HTTP_USER_AGENT')
        self.http = HTTP()

        class Query:
            path = environment.get('PATH_INFO')
            param = environment.get('QUERY_STRING')
            method = environment.get('REQUEST_METHOD')
            if param:
                full_path = '{}?{}'.format(path, param)
            else:
                full_path = path
        self.query = Query()

        class Client:
            address = environment.get('REMOTE_ADDR')
            hostname = environment.get('REMOTE_HOST')
        self.client = Client()

        class Script:
            name = environment.get('SCRIPT_NAME')
            pwd = environment.get('PWD')
            gateway_interface = environment.get('GATEWAY_INTERFACE')
        self.script = Script()

        class Server:
            name = environment.get('SERVER_NAME')
            port = environment.get('SERVER_PORT')
            protocol = environment.get('SERVER_PROTOCOL')
            software = environment.get('SERVER_SOFTWARE')
            shlvl = environment.get('SHLVL')
        self.server = Server()


class WSGIData:
    """ A model of the "wsgi.*" fields in the request data. """

    def __init__(self, environment):
        self.errors = environment.get('wsgi.errors')  # <_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>,
        self.file_wrapper = environment.get('wsgi.file_wrapper')  # <class 'wsgiref.util.FileWrapper'>
        self.input_file = environment.get('wsgi.input') # <_io.BufferedReader name=5>
        self.post_data = cgi.FieldStorage(fp=environment.get('wsgi.input'), environ=environment, keep_blank_values=True)
        self.multiprocess = environment.get('wsgi.multiprocess')
        self.multithread = environment.get('wsgi.multithread')
        self.run_once = environment.get('wsgi.run_once')
        self.url_scheme = environment.get('wsgi.url_scheme')
        self.version = environment.get('wsgi.version')
