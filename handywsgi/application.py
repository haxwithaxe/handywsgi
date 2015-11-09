

from genshi.template import TemplateLoader

from . import status


class Application:
    """ Application class for use with adapter.Adapter. """

    def __init__(self, config):
        self.config = config
        self.template_loader = TemplateLoader(self.config.template_path, auto_reload=True)
        self.template_extension = config.template_extension or '.html'

    def __call__(self, context):
        self.context = context
        method = self.context.request.query.method
        if method in ('GET', 'POST', 'PUT', 'HEAD', 'DELETE') and hasattr(self, method):
            content = getattr(self, method)(self.context)
            if content:
                self.content = content
            self.render(self.config.default_template)
        else:
            raise status.NoMethod(self)

    def format(self, template_name, **data):
        """ Render a template with data and return it. """
        content_template = self.template_loader.load(template_name+self.template_extension)
        content = content_template.generate(**data).render('html', doctype='html')
        return content

    def render(self, template_name):
        """ Render content and send it immediately. """
        page_template = self.template_loader.load(template_name+self.template_extension)
        page = page_template.generate(app=self).render('html', doctype='html')
        self.context.response.output.write(page)

    def dump(self, data):
        """ Dump data directly to the output buffer """
        self.context.response.output.write(data)
