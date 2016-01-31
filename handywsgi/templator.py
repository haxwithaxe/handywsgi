
import os
import tempfile

from lxml import etree
from genshi.template import TemplateLoader, MarkupTemplate, Template as BaseTemplate
from genshi.template.text import TextTemplate
from genshi import builder, HTML, XML




def create_xml_template(xml):
    stream = XML(etree.tostring(xml, encoding='utf-8'))
    return MarkupTemplate(stream)


def create_html_template(html):
    stream = HTML(etree.tostring(html, encoding='utf-8'))
    return MarkupTemplate(stream)


def create_text_template(html):
    stream = HTML(etree.tostring(html, encoding='utf-8'))
    return TextTemplate(stream)


def _dict_to_attrs(attrib_dict):
    attrs = []
    names = set()
    for name, value in attrib_dict.items():
        name = name.rstrip('_').replace('_', '-')
        if value is not None and name not in names:
            attrs.append((builder.QName(name), str(value)))
            names.add(name)
    return builder.Attrs(attrs)

def _attrs_to_dict(attrib):
    if len(attrib) == 1:
        return dict((attrib[0],))
    else:
        return dict(attrib)


class _AttributesAdapter:

    def __init__(self, tag):
        self.tag = tag

    def __contains__(self, key):
        return key in (x for x, y in self.tag.attrib)

    def __getitem__(self, key):
        attrib = _attrs_to_dict(self.tag.attrib)
        if key not in self:
            raise KeyError()
        return attrib[key]

    def __setitem__(self, key, value):
        key = builder.QName(key)
        attrib = _attrs_to_dict(self.tag.attrib)
        attrib[key] = value
        self.tag.attrib = _dict_to_attrs(attrib)

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def set(self, other):
        self.tag.attrib = _dict_to_attrs(other)

    def items(self):
        return _attrs_to_dict(self.tag.attrib).items()

    def values(self):
        return _attrs_to_dict(self.tag.attrib).values()

    def keys(self):
        return _attrs_to_dict(self.tag.attrib).keys()

    def update(self, attributes):
        for key, value in attributes.items():
            self[key] = value
    
    def get(self, key, default=None):
        if key in self:
            return self[key]
        else:
            return default

    def __str__(self):
        return str(_attrs_to_dict(self.tag.attrib))


class _ChildrenAdapter:

    def __init__(self, tag):
        self.tag = tag

    def _normalize_child(self, child):
        if hasattr(child, '__xml__'):
            return child.__xml__
        elif isinstance(child, str):
            return child
        elif isinstance(child, (int, float)):
            return str(child)
        elif isinstance(child, bool):
            return str(child).lower()

    def set(self, other):
        self.tag.children = other

    def append(self, child):
        if child is not None:
            norm = self._normalize_child(child)
            self.tag.children.append(norm)

    def extend(self, children):
        for child in children:
            self.append(child)

    def insert(self, index, child):
        self.tag.children.insert(index, child)

    def __contains__(self, key):
        return key in self.tag.children

    def __setitem__(self, index, child):
        if child is not None:
            self.tag.children[index] = self._normalize_child(child)

    def __getitem__(self, index):
        return self.tag.children[index]

    def __len__(self):
        return len(self.tag.children)

    def __str__(self):
        return str(self.tag.children)


class Tag:

    def __init__(self, tag, children=None, attributes=None):
        self.tag = getattr(builder.tag, tag)()
        self._children = _ChildrenAdapter(self.tag)
        self._attributes = _AttributesAdapter(self.tag)
        if children:
            if isinstance(children, (list, tuple)):
                self.children.extend(children)
            else:
                self.children.append(children)
        if attributes:
            if not isinstance(attributes, dict):
                raise TypeError()
            self.attributes.update(attributes)

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, other):
        self._attributes.set(other)

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, other):
        self._children.set(other)

    @property
    def __xml__(self):
        print('Tag', self.tag)
        return self.tag


class XMLSubTemplate(Tag):

    def __init__(self, tag, children=None, attributes=None):
        if isinstance(children, str):
            children = [children]
        elif isinstance(children, (list, tuple)):
            # Strip out falsey values
            children = [x for x in children if x]
        super().__init__(tag, attributes=attributes, children=children)

    
class TemplatingMixin:
    
    def __str__(self):
        if isinstance(self.template, BaseTemplate):
            return self.template.generate(**self.__dict__).render()
        else:
            template = Templator().loads(self.tempalte)
            return template.generate(**self.__dict__).render()


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
        return self._template.generate(**kwargs).render(
                self._render_type,
                doctype=self._doctype
                )


class Templator:
    """ A wrapper around genshi's TemplateLoader.

    The goal is to simplify the interface so the developer can focus on the function of the app and leave the shiny
    stuff for another day.

    Args:
        base_path (str): The path to the template directory relative or absolute. Defaults to ``'templates'``.

    """

    def __init__(self, base_path='templates', file_extension='html', auto_reload=True):
        self._base_path = base_path
        self._loader = TemplateLoader(self._base_path, auto_reload=auto_reload)
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

    def loads(self, template_string, file_type='xml'):
        factory = {
                'xml': create_xml_template,
                'html': create_html_template,
                'text': create_text_template
                }[file_type]
        return factory(template_string)

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
