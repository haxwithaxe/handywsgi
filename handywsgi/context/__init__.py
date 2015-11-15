
import io

import handywsgi.buffer

from .request import Request
from .response import Response, OutputContent


class Context:
    """ Encalsulation of request and response states. """

    def __init__(self, environment, start_response):
        self.request = Request(environment.copy())
        self.response = Response(start_response)

    def add_header(self, key, value, unique=False):
        """ Add a header based on the passed arguments. 
        
        See handywsgi.header.Headers for more details.

        """
        self.response.headers.add(key, value, unique)

    def set_output(self, filename):
        """ Set the output buffer to a file. """
        self.response.output = OutputContent(filename)
