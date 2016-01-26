#!/usr/bin/env python3

import wsgiref.simple_server

from handywsgi.adapter import Adapter
from handywsgi.application import Application
from handywsgi.session import Session


class DebugApp(Application):

    session = Session()

    def _on_request(self, context):
        self.session.load_cookies(context)
        print('got-cookies', self.session.cookies)
        if 'demo' not in self.session.cookies:
            self.session.add_cookie('demo', 'cookie demo', expires='never')
        print('set-cookies', self.session.cookies)
   
    def GET(self, context):
        self._on_request(context)
        self.content = None

    def POST(self, context):
        self._on_request(context)
        self.content = repr(context.request.wsgi.post_data)


class config:
    default_template = 'demo'
    template_path = './examples'
    template_extension = 'html'


httpd = wsgiref.simple_server.make_server('', 8000, Adapter({'debug': DebugApp(config())}))
print("Serving on port 8000...")

httpd.serve_forever()
