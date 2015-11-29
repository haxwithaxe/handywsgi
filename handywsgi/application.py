

from . import status, templator, HTTP_REQUEST_METHODS


class Application:
    """ Application class for use with adapter.Adapter. """

    def __init__(self, config):
        self.config = config
        self.templator = templator.Templator(
                self.config.template_path,
                self.config.template_extension or 'html'
                )
        self.context = None
        self.content = None

    def __call__(self, context):
        self.context = context
        method = self.context.request.query.method
        if method in HTTP_REQUEST_METHODS and hasattr(self, method):
            content = getattr(self, method)(self.context)
            if content:
                self.content = content
            self.render(self.config.default_template)
        else:
            raise status.NoMethod(self)

    def format(self, template_name=None, **data):
        """ Render a template with data and return it. """
        if not template_name:
            template_name = self.config.default_template
        content = self.templator.render(template_name, **data)
        return content

    def render(self, template_name=None):
        """ Render content and send it immediately. """
        if not template_name:
            template_name = self.config.default_template
        template = self.templator.get_template(template_name)
        page = template.render(app=self)
        self.context.response.output.write(page)

    def dump(self, data):
        """ Dump data directly to the output buffer """
        self.context.response.output.write(data)

