
import io

import handywsgi.buffer

from .request import Request
from .response import Response, Content


class Context:
    """ Encalsulation of request and response. """

    def __init__(self, environment, start_response):
        self.request = Request(environment.copy())
        self.response = Response(start_response)

    def add_header(self, key, value, unique=False):
        self.response.headers.add(key, value, unique)

    def set_output(self, filename):
        self.response.output = Content(filename)

