
import http.cookies


DEFAULT_MORSEL_OPTIONS = {'expires': None, 'path': None, 'comment': None, 'domain': None, 'max-age': None, 'secure': False, 'version': None, 'httponly': False}

def _scrub_underscores(kwargs):
    return { key.replace('_', '-'): value for key, value in kwargs.items()}

class Session:

    def __init__(self):
        self.cookies = http.cookies.SimpleCookie()
        self.session_state = {'page': None }

    def load_cookies(self, context):
        self.cookies.load(context.request.environment.get('HTTP_COOKIE', ''))
        self.cookies.load(context.request.environment.get('Cookie', ''))

    def __getstate__(self):
        return {'cookies': str(self.cookies), 'sessoin_state': self.session_state}

    def __stestate__(self, state):
        self.cookies.load(state.get('cookies', ''))
        self.session_state = state.get('session_state', {})

    def remove_cookie(self, name):
        pass

    def update_cookie(self, name, **values):
        if 'value' in values:
            value = values.pop('value')
            self.cookies[name] = value
        self.cookies[name].update(_scrub_underscores(values))

    def add_cookie(self, name, value, **kwargs):
        """

        Keyword Arguments:
            expires=None
            path=None
            comment=None
            domain=None
            max-age=None
            secure=False
            version=None
            httponly=False

        """
        self.cookies[name] = value
        fields = DEFAULT_MORSEL_OPTIONS.copy()
        fields.update(_scrub_underscores(kwargs))
        for field, field_value in fields.items():
            if field in ('httponly', 'secure') and not field_value:
                continue
            if field_value is not None:
                self.cookies[name][field] = field_value
