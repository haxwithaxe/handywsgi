
import os
import tempfile

from genshi.template import TemplateLoader


class TemplatingMixin:
    
    template = None
    tempfile_path = '/tmp/'

    def __str__(self):
        template = Templator(self.tempfile_path, autoreload=False).loads(self.tempalte)
        return template.render(**self.__dict__)


class Template:
    """ A simplified reusable template interface.

    Args:
        template (genshi.template.Template): 
        render_type: The rendering method to use for rendering the template. Defaults to 'html'.
        doctype: The doctype of the template. Defaults to 'html'.

    """

    def __init__(self, template, render_type='html', doctype='html'):
        self._template = template
        self._render_type = render_type
        self._doctype = doctype

    def render(self, **kwargs):
        """ Return a rendered template.

        Keyword Arguments:
            ...: whatever your template needs to know.

        Returns:
            str: Return a rendered template.

        """
        return self._template.generate(**kwargs).render(self._render_type,
                                                       doctype=self._doctype)


class Templator:
    """ A wrapper around genshi's TemplateLoader.

    The goal is to simplify the interface so the developer can focus on the function of the app and leave the shiny
    stuff for another day.

    Args:
        base_path (str): The path to the template directory relative or absolute. Defaults to ``'templates'``.

    """

    def __init__(self, base_path='templates', file_extension='html', auto_reload=True):
        self._base_path = base_path
        self._loader = TemplateLoader(self.base_path, auto_reload=auto_reload)
        self._file_extension = file_extension

    def load(self, name, file_extension=None):
        """ Returns a ``Template`` instance.

        Args:
            file_extension (str): An override for the ``file_extension`` instance attribute.

        """
        return Template(
                self._loader.load(
                        '%s.%s' % (name, file_extension or self._file_extension)
                        )
                )

    def loads(self, template_string):
        file_obj, path = tempfile.mkstemp(suffix=self._file_extension, prefix=self._base_path)
        with file_obj as template_file:
            os.write(template_file, template_string.encode('utf-8'))
        return self.load(path)

    def render(self, name, **kwargs):
        """ Shortcut for rendering a template.

        Args:
            name (str): The template name (without file extension).

        Keyword Arguments:
            file_extension (str): The filename extension of the template. Defaults to 'html'.
            render_type (str): The rendering method to be used with the template. Defaults to 'html'.
            doctype (str): The doctype of the template. Defaults to 'html'.
            ...: The remaining keyword arguments are passed directly to the template.

        Returns:
            str: The rendered template.

        """
        file_extension = 'html'
        render_type = 'html'
        doctype = 'html'
        # Remove the keywords meant for this method and not for the template.
        if 'file_extension' in kwargs:
            file_extension = kwargs.pop('file_extension')
        if 'doctype' in kwargs:
            doctype = kwargs.pop('doctype')
        if 'render_type' in kwargs:
            render_type = kwargs.pop('render_type')
        template = Template(self._loader.load('%s.%s' % (name, file_extension)),
                            render_type=render_type,
                            doctype=doctype)
        return template.render(**kwargs)

if __name__ == '__main__':
    print(Templator('./').render('hello', title='Hello world', message='ohai thar!'))
