
import os

from .context import Context
from . import status


class Adapter:
    """ A WSGI to app adapter.

    Attributes:
        storage (dict):

    """

    def __init__(self, apps, default_app=None):
        self._apps = apps
        self._apps[''] = default_app or self._index
        self.storage = {}

    def _index(self, context):
        """ Creates an index page based on apps in the ``Adapter`` instance. """
        page = ['<head><title>HandyWSGI</title></head><h1>Index</h1>']
        for path in [x for x in self._apps if x]:
            page.append('<div><a href="/{path}">{path}</a></div>'.format(
                    path=path
                    ))
        context.response.output.write(''.join(page))

    def __call__(self, environ, start_response):
        """ WSGI entry point. """
        context = Context(environ, start_response)
        raw_uri_path = context.request.query.path
        uri_path = raw_uri_path.strip('/').strip()
        if uri_path not in self._apps:
            uri_path = os.path.dirname(uri_path)
            if uri_path not in self._apps:
                context.response.status = status.NotFound(uri_path or '/')
        app = self._apps.get(uri_path, self._index)
        self._run_app(app, context)
        start_response(
                context.response.status.status,
                context.response.headers.items()
                )
        return [context.response.output.read_bytes()]

    def _run_app(self, app, context):
        """ Run the selected app and handler errors. """
        try:
            app(context)
        except status.HTTPStatus as stat:
            context.response.status = stat.status
            context.response.headers = stat.headers
            context.response.output.clear()
            context.response.output.write(stat.message)
