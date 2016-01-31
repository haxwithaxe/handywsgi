

from handywsgi import form


class TextArea(form.SimpleTag):
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

    tag_string = form.TEXTAREA


class LabeledTextArea(form.SimpleLabeledTag):

    tag_string = form.TEXTAREA
