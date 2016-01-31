
from handywsgi import form


class Select(form.FormElement):
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

    def __init__(self, options, flags=None, attributes=attributes, **kwargs):
        for index, option in enumerate(options):
            if isinstance(option, dict):
                options[index] = Option(**option)
        super().__init__(form.SELECT, options, flags=flags, attributes=attributes, **kwargs)


class Option(form.SimpleTag):
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

    tag_string = form.OPTION
