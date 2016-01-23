
from handywsgi.templator import TemplatingMixin


TEXTAREA = 'textarea'
INPUT = 'input'
BUTTON = 'button'
SUBMIT = 'submit'
RESET = 'reset'
DISABLED = 'disabled'
READONLY = 'readonly'
SELECT = 'select'
OPTION = 'option'
SELECTED = 'selected'
CHECKED = 'checked'
TEXT = 'text'
PASSWORD = 'password'
CHECKBOX = 'checkbox'
RADIO = 'radio'
FILE = 'file'
HIDDEN = 'hidden'
IMAGE = 'image'


def bool_to_text(value, true_text, false_text):
    return {True: true_text, False: false_text}[value]


def expand_boolean_attribute(attribute, value=True):
    if value:
        return (attribute, attribute)
    else:
        return (None, None)


class FormElement(TemplatingMixin):

    template = '''<%%%tag%%% py:attrs="attributes">
        ${children}
        </%%%tag%%%>'''

    _attrib_template = {
        'id': None,
        'class': None,
        'lang': None,
        'dir': None,
        'title': None,
        'style': None,
        'disabled': None,
        'accesskey': None,
        'tabindex': None
        }

    def __init__(self, tag, children, *boolean_attributes, **attributes):
        self.template = self.template.replace('%%%tag%%%', tag)
        self._children = children
        self._attributes = attributes
        if 'element_type' in self._attributes:
            self._attributes['type'] = self._attributes.pop('element_type')
        self._add_boolean_attributes(boolean_attributes)

    def _add_boolean_attributes(self, attributes):
        for x in attributes:
            key, value = expand_boolean_attribute(x)
            if None in (key, value):
                continue
            self._attributes[key] = value

    def _validate_one_of(self, attribute, options, required=False):
        if attribute in self._attributes:
            if self._attributes.get(attribute) not in options:
                raise TypeError('Attribute %s must be one of: %s' % (attribute, ', '.join([str(x) for x in options])))
        elif required:
            raise TypeError('Missing required attribute: %s' % attribute)

    def _validate_type(self, attribute, value_type, required=False):
        if attribute in self._attributes:
            if not isinstance(self._attributes.get(attribute), value_type):
                raise TypeError('Attribute %s must be of type: %s' % (attribute, value_type))
        elif required:
            raise TypeError('Missing required attribute: %s' % attribute)

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        if not self._attributes:
            self._attributes = self._attrib_template.copy()
        if isinstance(attributes, (list, tuple)):
            self._add_boolean_attributes(attributes)
        else:
            self._attributes.update(attributes)

    def __dict__(self):
        attributes = {x: str(y) for x, y in self.attributes.copy().keys() if x and y is not None}
        return {'children': self._children, 'attributes': attributes}

    def __getattr__(self, attr):
        if attr in self._attributes:
            return self._attributes[attr]
        raise AttributeError(attr)


class Label(FormElement):

    def __init__(self, text, *boolean_attributes, **attributes):
        super().__init__('label', [text], *boolean_attributes, **attributes)

    def wrap(self, element):
        self._children.append(element)


class Input(FormElement):
    """
  type        %InputType;    TEXT      -- what kind of widget is needed --
  checked     (checked)      #IMPLIED  -- for radio buttons and check boxes --
  disabled    (disabled)     #IMPLIED  -- unavailable in this context --
  readonly    (readonly)     #IMPLIED  -- for text and passwd --
  maxlength   NUMBER         #IMPLIED  -- max chars for text fields --
  ismap       (ismap)        #IMPLIED  -- use server-side image map --
  tabindex    NUMBER         #IMPLIED  -- position in tabbing order --
  accept      %ContentTypes; #IMPLIED  -- list of MIME types for file upload --

    """

    def __init__(self, *boolean_attributes, **attributes):
        super().__init__('input', [], *boolean_attributes, **attributes)
        self._validate_type('type', (TEXT, PASSWORD, CHECKBOX, RADIO, SUBMIT, RESET, FILE, HIDDEN, IMAGE, BUTTON))


class Select(FormElement):
    """

<!ELEMENT SELECT - - (OPTGROUP|OPTION)+ -- option selector -->
<!ATTLIST SELECT
  %attrs;                              -- %coreattrs, %i18n, %events --
  name        CDATA          #IMPLIED  -- field name --
  size        NUMBER         #IMPLIED  -- rows visible --
  multiple    (multiple)     #IMPLIED  -- default is single selection --
  disabled    (disabled)     #IMPLIED  -- unavailable in this context --
  tabindex    NUMBER         #IMPLIED  -- position in tabbing order --
  onfocus     %Script;       #IMPLIED  -- the element got the focus --
  onblur      %Script;       #IMPLIED  -- the element lost the focus --
  onchange    %Script;       #IMPLIED  -- the element value was changed --
  %reserved;                           -- reserved for possible future use --
  >
    """

    def __init__(self, options, *boolean_attributes, **attributes):
        super().__init__(SELECT, options, *boolean_attributes, **attributes)


class Option(FormElement):
    """
<!ELEMENT OPTION - O (#PCDATA)         -- selectable choice -->
<!ATTLIST OPTION
  %attrs;                              -- %coreattrs, %i18n, %events --
  selected    (selected)     #IMPLIED
  disabled    (disabled)     #IMPLIED  -- unavailable in this context --
  label       %Text;         #IMPLIED  -- for use in hierarchical menus --
  value       CDATA          #IMPLIED  -- defaults to element content --
  >
    """

    def __init__(self, label, value, selected=False, disabled=False):
        super().__init__(OPTION, None, value=value, label=label)
        if selected:
            self.attributes.update({SELECTED: SELECTED})
        if disabled:
            self.attributes.update({DISABLED: DISABLED})



class TextArea(FormElement):
    """
<!ELEMENT TEXTAREA - - (#PCDATA)       -- multi-line text field -->
<!ATTLIST TEXTAREA
  %attrs;                              -- %coreattrs, %i18n, %events --
  name        CDATA          #IMPLIED
  rows        NUMBER         #REQUIRED
  cols        NUMBER         #REQUIRED
  disabled    (disabled)     #IMPLIED  -- unavailable in this context --
  readonly    (readonly)     #IMPLIED
  tabindex    NUMBER         #IMPLIED  -- position in tabbing order --
  accesskey   %Character;    #IMPLIED  -- accessibility key character --
  onfocus     %Script;       #IMPLIED  -- the element got the focus --
  onblur      %Script;       #IMPLIED  -- the element lost the focus --
  onselect    %Script;       #IMPLIED  -- some text was selected --
  onchange    %Script;       #IMPLIED  -- the element value was changed --
  >
    """

    def __init__(self, default_text, *boolean_attributes, **attributes):
        super().__init__(TEXTAREA, default_text, *boolean_attributes, **attributes)
        self._validate_type('rows', int)
        self._validate_type('cols', int)


class Button(FormElement):
    """

    name        CDATA          #IMPLIED
    value       CDATA          #IMPLIED  -- sent to server when submitted --
    type        (button|submit|reset) submit -- for use as form button --
    disabled    (disabled)     #IMPLIED  -- unavailable in this context --
    tabindex    NUMBER         #IMPLIED  -- position in tabbing order --
    accesskey   %Character;    #IMPLIED  -- accessibility key character --
    onfocus     %Script;       #IMPLIED  -- the element got the focus --
    onblur      %Script;       #IMPLIED  -- the element lost the focus --

    """

    def __init__(self, *boolean_attributes, **attributes):
        super().__init__('button', None, *boolean_attributes, **attributes)
        self._validate_one_of('type', (BUTTON, SUBMIT, RESET), required=True)


class Group(FormElement):
    """ 
    
    Args:
        label (str): Text label for the group.
        elements (tuple): A tuple of FormElement instances.

    """

    def __init__(self, label, elements, *boolean_attributes, **attributes):
        super().__init__('div', elements, *boolean_attributes, **attributes)
        self._label = label

    def __dict__(self):
        dict_self = super().__dict__
        dict_self['label'] = self._label
        return dict_self

class RadioGroup(Group):

    def __init__(self, name, options, *boolean_attributes, default_option=None, **attributes):
        children = []
        for value, text in options.items():
            if default_option == value:
                children.append(Input(RADIO, [text], CHECKED, name=name, value=value))
            else:
                children.append(Input(RADIO, [text], CHECKED, name=name, value=value))
        super().__init__(None, children, *boolean_attributes, **attributes)


class CheckboxGroup(Group):

    def __init__(self, name, options, *boolean_attributes, default_option=None, **attributes):
        children = []
        for value, text in options.items():
            if default_option == value:
                children.append(Input(CHECKBOX, [text], CHECKED, name=name, value=value))
            else:
                children.append(Input(CHECKBOX, [text], name=name, value=value))
        super().__init__(None, children, *boolean_attributes, **attributes)

