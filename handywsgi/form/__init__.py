
from handywsgi.templator import Tag, XMLSubTemplate

FORM = 'form'
METHOD = 'method'
GET = 'get'
POST = 'post'
TEXTAREA = 'textarea'
TEXT = 'text'
EMAIL = 'email'
FIELDSET = 'fieldset'
LEGEND = 'legend'
LABEL = 'label'
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
PASSWORD = 'password'
CHECKBOX = 'checkbox'
RADIO = 'radio'
FILE = 'file'
HIDDEN = 'hidden'
IMAGE = 'image'
TYPE = 'type_'
ROWS = 'rows'
COLS = 'cols'
VALUE = 'value'
PARAGRAPH = 'p'
DIV = 'div'


def _extract_from_kwargs(key, kwargs):
    if key in kwargs:
        return kwargs.pop(key)


def bool_to_text(value, true_text, false_text):
    return {True: true_text, False: false_text}[value]


def expand_boolean_attribute(attribute, value=True):
    if value is True:
        return (attribute, attribute)
    elif isinstance(value, str):
        return (attribute, attribute)
    else:
        return (None, None)


def boolean_attributes_to_dict(attributes):
    attributes_dict = {}
    for x in attributes:
        key, value = expand_boolean_attribute(x)
        if None in (key, value):
            continue
        attributes_dict[key] = value
    return attributes_dict


def _clean_attributes(attributes):
    for key in attributes.keys():
        if key[-1] == '_':
            attributes[key.strip('_')] = attributes.pop(key)
    return attributes


class BooleanAttributesMixin:

    def validate_boolean_attribute(self, attribute, required=False):
        if attribute in self._tag:
            value = self._tag[attribute]
            return value == attribute or isinstance(value, (bool, str))
        elif required:
            return False
        return None

    def validate_type(self, attribute, value_type, required=False):
        if attribute in self._tag:
            return isinstance(self._tag.get(attribute), value_type)
        elif required:
            return False
        return None

    def validate_one_of(self, attribute, options, required=False):
        if attribute in self._tag:
            return self._tag.get(attribute) in options
        elif required:
            return False
        return None

    def _set_bool_attribute(self, key, value):
        if value:
            self._tag.update({key: key})
        elif key in self._tag:
            del self._tag[key]

    def _get_bool_attribute(self, key):
        return bool(self._tag.get(key))

    @property
    def selected(self):
        return self._get_bool_attribute(SELECTED)

    @selected.setter
    def selected(self, value):
        self._set_bool_attribute(SELECTED, value)

    @property
    def disabled(self):
        return self._get_bool_attribute(DISABLED)

    @disabled.setter
    def disabled(self, value):
        self._set_bool_attribute(DISABLED, value)

    @property
    def checked(self):
        return self._get_bool_attribute(CHECKED)

    @checked.setter
    def checked(self, value):
        self._set_bool_attribute(CHECKED, value)

    @property
    def readonly(self):
        return self._get_bool_attribute(READONLY)

    @readonly.setter
    def readonly(self, value):
        self._set_bool_attribute(READONLY, value)


class FormElement(XMLSubTemplate, BooleanAttributesMixin):

    def __init__(self, tag, children=None, boolean_attributes=None, attributes=None):
        attributes = _clean_attributes(attributes or {})
        print('%s.__init__ attributes' % self.__class__.__name__, attributes)
        XMLSubTemplate.__init__(
                self,
                tag,
                children=children,
                attributes=attributes or {}
                )
        if boolean_attributes:
            print('boolean_attributes', boolean_attributes)
            self._tag.update(boolean_attributes_to_dict(boolean_attributes or ()))

    def validate_one_of(self, attribute, options, required=False):
        if super().validate_one_of(attribute, options, required) is False:
            raise TypeError('Attribute %s must be one of: %s' % (attribute, ', '.join([str(x) for x in options])))

    def validate_boolean_attribute(self, attribute, required=False):
        if super().validate_boolean_attribute(attribute, required) is False:
            raise TypeError('Attribute %s must either be of type bool or be truethy or falsey.' % attribute)

    def validate_type(self, attribute, value_type, required=False):
        if super().validate_type(attribute, value_type, required) is False:
            raise TypeError('Attribute %s must be of type: %s' % (attribute, value_type))

    def append(self, child_element):
        self._tag.append(child_element)


class Form(FormElement):
    """

    <!ELEMENT FORM - - (%block;|SCRIPT)+ -(FORM) -- interactive form -->
    <!ATTLIST FORM
      %attrs;                              -- %coreattrs, %i18n, %events --
      action      %URI;          #REQUIRED -- server-side form handler --
      method      (GET|POST)     GET       -- HTTP method used to submit the form--
      enctype     %ContentType;  "application/x-www-form-urlencoded"
      accept      %ContentTypes; #IMPLIED  -- list of MIME types for file upload --
      name        CDATA          #IMPLIED  -- name of form for scripting --
      onsubmit    %Script;       #IMPLIED  -- the form was submitted --
      onreset     %Script;       #IMPLIED  -- the form was reset --
      accept-charset %Charsets;  #IMPLIED  -- list of supported charsets --
      >

    """

    def __init__(self, elements, *boolean_attributes, **attributes):
        super().__init__(FORM, children=elements, boolean_attributes=boolean_attributes, attributes=attributes)
        self.validate_one_of(METHOD, (GET, POST))


class Label(FormElement):

    def __init__(self, text, children=None, boolean_attributes=None, attributes=None):
        super().__init__(LABEL, boolean_attributes=boolean_attributes, attributes=attributes)
        if text:
            self.wrap(text)
        if children:
            self.wrap(children)

    def wrap(self, element):
        self.append(element)


class Input(FormElement, BooleanAttributesMixin):
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

    def __init__(self, element_type, children=None, boolean_attributes=None, attributes=None):
        attributes['type'] = element_type
        super().__init__(INPUT, boolean_attributes=boolean_attributes, attributes=attributes)
        #self.validate_one_of(TYPE, (TEXT, PASSWORD, CHECKBOX, RADIO, SUBMIT, RESET, FILE, HIDDEN, IMAGE, BUTTON))
        self.validate_boolean_attribute(CHECKED)
        self.validate_boolean_attribute(DISABLED)
        self.validate_boolean_attribute(READONLY)


class Button(FormElement, BooleanAttributesMixin):
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

    def __init__(self, title, *boolean_attributes, **attributes):
        super().__init__(BUTTON, children=title, boolean_attributes=boolean_attributes, attributes=attributes)


class FieldSet(FormElement):
    """

    Args:
        elements (tuple): A tuple of FormElement instances.

    """

    def __init__(self, label, elements, *boolean_attributes, **attributes):
        super().__init__(FIELDSET, label, boolean_attributes=boolean_attributes, attributes=attributes)
        self.append(elements)


class Group(FormElement):
    """

    Args:
        elements (tuple): A tuple of FormElement instances.

    """

    def __init__(self, elements, *boolean_attributes, **attributes):
        super().__init__(DIV, children=elements, boolean_attributes=boolean_attributes, attributes=attributes)


class P(FormElement):
    """

    Args:
        elements (tuple): A tuple of FormElement instances.

    """

    def __init__(self, elements, *boolean_attributes, **attributes):
        super().__init__(PARAGRAPH, children=elements, boolean_attributes=boolean_attributes, attributes=attributes)
