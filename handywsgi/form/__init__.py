
from handywsgi.templator import Tag, XMLSubTemplate


# <form/>
FORM = 'form'
METHOD = 'method'
GET = 'get'
POST = 'post'
ENCTYPE = 'enctype'

# <textarea/>
TEXTAREA = 'textarea'
ROWS = 'rows'
COLS = 'cols'

# <input/>
INPUT = 'input'
TEXT = 'text'
PASSWORD = 'password'
CHECKBOX = 'checkbox'
RADIO = 'radio'
# SUBMIT
# RESET
FILE = 'file'
HIDDEN = 'hidden'
IMAGE = 'image'
# BUTTON

FIELDSET = 'fieldset'
LEGEND = 'legend'
LABEL = 'label'

# <button/>
BUTTON = 'button'
SUBMIT = 'submit'
RESET = 'reset'

DISABLED = 'disabled'
READONLY = 'readonly'

# <select/>
SELECT = 'select'
OPTION = 'option'
# OPTGROUP

# Random attributes
SELECTED = 'selected'
CHECKED = 'checked'
TYPE = 'type'
VALUE = 'value'


def merge_attributes(attributes, flags, kwargs):
    attributes = attributes or {}
    attributes.update(kwargs)
    clean_attributes = _clean_attributes(attributes)
    if flags:
        clean_attributes.update(_flags_to_dict(flags))
    return clean_attributes


def pull_reserved_kwargs(prefix, kwargs):
    child_attributes = {}
    attributes = {}
    for key, value in kwargs.items():
        if key.startswith(prefix):
            attributes[key.replace(prefix, '')] = value
        else:
            child_attributes[key] = value
    return attributes, child_attributes


def _extract_from_kwargs(key, kwargs):
    if key in kwargs:
        return kwargs.pop(key)


def _expand_flag(flag, value=True):
    """ Normalize flag attributes for use as regular attributes.
    
    Translate attributes with xhtml-truethy values into normalized boolean attributes.
    
    Example:
        >>> _expand_flag('selected')
        ('selected', 'selected')
        >>> _expand_flag_attribute('selected', True)
        ('selected', 'selected')
        >>> _expand_flag_attribute('disabled', False)
        (None, None)

    """
    if value is True:
        return (flag, flag)
    elif isinstance(value, str):
        return (flag, flag)
    else:
        return (None, None)


def _flags_to_dict(flags):
    """ Turn a list of attribute names and turn them into regular attributes.
    
    This turns attributes that in HTML originally were only flags and didn't need values into key-value-pairs with key
    being used as the value.
    
    """
    attributes = {}
    for x in flags:
        key, value = _expand_flag(x)
        if None in (key, value):
            continue
        attributes[key] = value
    return attributes


def _clean_attributes(attributes):
    """ Strip trailing ``_`` from keyword arguments (eg `**attributes`). """
    for key in attributes.keys():
        if key[-1] == '_':
            attributes[key.strip('_')] = attributes.pop(key)
    return attributes



class FlagsMixin:

    def validate_flag(self, flag, required=False):
        if flag in self.attributes:
            value = self.attributes[flag]
            return value == flag or isinstance(value, (bool, str))
        elif required:
            return False
        return None

    def validate_type(self, attribute, value_type, required=False):
        if attribute in self.attributes:
            return isinstance(self.attributes.get(attribute), value_type)
        elif required:
            return False
        return None

    def validate_one_of(self, attribute, options, required=False):
        if attribute in self.attributes:
            return self.attributes.get(attribute) in options
        elif required:
            return False
        return None

    def _set_flag(self, flag, value):
        key, value = _expand_flag(flag, value)
        if value:
            self.attributes.update({flag: flag})
        elif flag in self.attributes:
            del self.attributes[flag]

    def _get_flag(self, flag):
        return bool(self.attributes.get(flag))

    def _make_flag_getter(self, flag):
        return lambda: self._get_flag(flag)

    def _make_flag_setter(self, flag):
        return lambda value: self._set_flag(flag, value)

    def _make_flag_property(self, flag):
        prop = property(self._make_flag_getter(flag), self._make_flag_setter(flag))
        setattr(self, flag, prop)


class FormElement(XMLSubTemplate, FlagsMixin):

    hardcoded_attributes = {}
    _reserved_kwarg_prefix = None

    def __init__(
            self,
            tag,
            children=None,
            flags=None,
            attributes=None,
            **kwargs
            ):
        super().__init__(tag, children=children)
        attributes = merge_attributes(attributes, flags, kwargs)
        self.attributes.update(attributes)
        if self.hardcoded_attributes:
            self.attributes.update(self.hardcoded_attributes)


    def validate_one_of(self, attribute, options, required=False):
        if super().validate_one_of(attribute, options, required) is False:
            raise TypeError(
                    'Attribute %s must be one of: %s' %
                    (attribute, ', '.join([str(x) for x in options]))
                    )

    def validate_flag(self, flag, required=False):
        if super().validate_flag(flag, required) is False:
            raise TypeError(
                    'Attribute %s must either be of type bool or be truethy'
                    ' or falsey.' % flag
                    )

    def validate_type(self, attribute, value_type, required=False):
        if super().validate_type(attribute, value_type, required) is False:
            raise TypeError(
                    'Attribute %s must be of type: %s' % (attribute, value_type)
                    )

    def append(self, child_element):
        self.children.append(child_element)

    def extend(self, *child_elements):
        self.children.extend(child_elements)

    def wrap(self, element):
        if isinstance(element, (list, tuple)):
            self.extend(element)
        else:
            self.append(element)

    def update(self, key_value_pairs):
        self.attributes.update(key_value_pairs)

    @property
    def first_child(self):
        try:
            return self.children[0]
        except IndexError:
            return None

    @first_child.setter
    def first_child(self, child):
        self.children.insert(0, child)

    @property
    def __xml__(self):
        return self.tag


class SimpleTag(FormElement):

    tag_string = None

    def __init__(self, children=None, flags=None, **attributes):
        super().__init__(self.tag_string, children=children, flags=flags, attributes=attributes)


class Div(SimpleTag):

    tag_string = 'div'


class Legend(SimpleTag):

    tag_string = 'legend'


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

    def __init__(self, elements=None, flags=None, attributes=None, **kwargs):
        super().__init__(FORM, children=elements, flags=flags, attributes=attributes, **kwargs)
        if not ENCTYPE in self.attributes:
            self.attributes.update({ENCTYPE: 'multipart/form-data'})
        self.validate_one_of(METHOD, (GET, POST))


class Label(FormElement):

    child_tag = None
    reserved_kwarg_prefix = 'label_'

    def __init__(self, text, children=None, flags=None, attributes=None, **kwargs):
        parent_attributes, child_attributes = pull_reserved_kwargs(self.reserved_kwarg_prefix, merge_attributes(attributes, flags, kwargs))
        super().__init__(LABEL, children=children, flags=flags, attributes=parent_attributes)
        if text:
            self.first_child = text
        if callable(self.child_tag):
            child = self.child_tag(flags=flags, attributes=child_attributes)
            self.children.append(child)


class SimpleLabeledTag(Label):
    """ Base class to make elements wrapped in a label.
    
    Keyword arguments prefixed with `label_` are stripped of their prefix and passed to the Label.
        
    """
    
    label_hardcoded_attributes = {}
    tag_string = None

    def __init__(self, label=None, attributes=None, **kwargs):
        class TagClass(SimpleTag):
            tag_string = self.tag_string
            hardcoded_attributes = self.hardcoded_attributes.copy()
        self.hardcoded_attributes = self.label_hardcoded_attributes
        self.child_tag = TagClass
        super().__init__(text=label, attributes=attributes, **kwargs)


class Input(FormElement):
    """ Input widget base class.

    Note:
        From W3C:
            <!ENTITY % InputType
              "(TEXT | PASSWORD | CHECKBOX |
                RADIO | SUBMIT | RESET |
                FILE | HIDDEN | IMAGE | BUTTON)"
               >

            <!-- attribute name required for all but submit and reset -->
            <!ELEMENT INPUT - O EMPTY              -- form control -->
            <!ATTLIST INPUT
              %attrs;                              -- %coreattrs, %i18n, %events --
              type        %InputType;    TEXT      -- what kind of widget is needed --
              name        CDATA          #IMPLIED  -- submit as part of form --
              value       CDATA          #IMPLIED  -- Specify for radio buttons and checkboxes --
              checked     (checked)      #IMPLIED  -- for radio buttons and check boxes --
              disabled    (disabled)     #IMPLIED  -- unavailable in this context --
              readonly    (readonly)     #IMPLIED  -- for text and passwd --
              size        CDATA          #IMPLIED  -- specific to each type of field --
              maxlength   NUMBER         #IMPLIED  -- max chars for text fields --
              src         %URI;          #IMPLIED  -- for fields with images --
              alt         CDATA          #IMPLIED  -- short description --
              usemap      %URI;          #IMPLIED  -- use client-side image map --
              ismap       (ismap)        #IMPLIED  -- use server-side image map --
              tabindex    NUMBER         #IMPLIED  -- position in tabbing order --
              accesskey   %Character;    #IMPLIED  -- accessibility key character --
              onfocus     %Script;       #IMPLIED  -- the element got the focus --
              onblur      %Script;       #IMPLIED  -- the element lost the focus --
              onselect    %Script;       #IMPLIED  -- some text was selected --
              onchange    %Script;       #IMPLIED  -- the element value was changed --
              accept      %ContentTypes; #IMPLIED  -- list of MIME types for file upload --
              >

    """

    def __init__(self, element_type=None, children=None, flags=None, attributes=None, **kwargs):
        super().__init__(INPUT, children=children, flags=flags, attributes=attributes, **kwargs)
        if attributes and TYPE not in attributes:
            self.attributes.update({TYPE: element_type})
        self.validate_one_of(TYPE, (TEXT, PASSWORD, CHECKBOX, RADIO, SUBMIT, RESET, FILE, HIDDEN, IMAGE, BUTTON))
        self.validate_flag(CHECKED)
        self.validate_flag(DISABLED)
        self.validate_flag(READONLY)


class Button(FormElement):
    """ 

    Arguments:
        value (str, optional): The text displayed on the button. Defaults to the button type.
        flags (tuple or str, optional): A tuple or string representing HTML element flags.
        attributes (dict, optional): HTML attributes.
    
    Keyword Arguments:
        HTML attributes as key-value-pairs.
    
    Note:
        From W3C:
            <!ELEMENT BUTTON - -
                 (%flow;)* -(A|%formctrl;|FORM|FIELDSET)
                 -- push button -->
            <!ATTLIST BUTTON
              %attrs;                              -- %coreattrs, %i18n, %events --
              name        CDATA          #IMPLIED
              value       CDATA          #IMPLIED  -- sent to server when submitted --
              type        (button|submit|reset) submit -- for use as form button --
              disabled    (disabled)     #IMPLIED  -- unavailable in this context --
              tabindex    NUMBER         #IMPLIED  -- position in tabbing order --
              accesskey   %Character;    #IMPLIED  -- accessibility key character --
              onfocus     %Script;       #IMPLIED  -- the element got the focus --
              onblur      %Script;       #IMPLIED  -- the element lost the focus --
              >

    """

    def __init__(self, value=None, flags=None, attributes=None, **kwargs):
        super().__init__(BUTTON, flags=flags, attributes=attributes, **kwargs)
        value = value or self.attributes[TYPE]
        self.attributes.update({VALUE: value})
        self.children.append(value)


class FieldSet(FormElement):
    """

    Arguments:
        legend (str): Legend text.
        elements (tuple): A tuple of FormElement instances.
        flags (tuple or str): A tuple or string representing HTML element flags.
        attributes: HTML attributes.
    
    Keyword Arguments:
        HTML attributes as key-value-pairs.

    """

    def __init__(self, legend=None, elements=None, flags=None, attributes=None, **kwargs):
        super().__init__(FIELDSET, children=elements, flags=flags, attributes=attributes, **kwargs)
        if legend:
            self.first_child = Legend(legend)


class BaseGroup(FieldSet):
    """ Element group base class.
    
    Arguments:
        options (list): A list of dict objects representing keyword arguments for the grouped element type.
        legend (str): Text value for the legend.
        labeled (bool): If True the labeled versionof the grouped element type is used.
        attributes: HTML element attributes.
        
    Keyword Arguments:
        HTML attributes as key-value-pairs.
        
    """

    plain_type = None
    labeled_type = None
    _element_classes = {True: labeled_type, False: plain_type}

    def __init__(self, options, legend=None, labeled=False, attributes=None, **kwargs):
        super().__init__(legend=legend, attributes=attributes or kwargs)
        self._legend = legend
        for option in options:
            self.append(self._element_classes[labeled](**option))
