

from handywsgi import form

class TextArea(form.FormElement, form.BooleanAttributesMixin):
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
    >

    """

    def __init__(self, default_text, *boolean_attributes, **attributes):
        super().__init__(
                form.TEXTAREA,
                children=default_text,
                boolean_attributes=boolean_attributes,
                attributes=attributes)
        self.validate_type(form.ROWS, int)
        self.validate_type(form.COLS, int)


class LabeledTextArea(form.Label):

    def __init__(
            self,
            label,
            default_text,
            *boolean_attributes,
            label_attributes={},
            **attributes
            ):
        super().__init__(label, **label_attributes)
        textarea = TextArea(default_text, *boolean_attributes, **attributes)
        self.wrap(textarea)
