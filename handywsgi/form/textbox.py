
from handywsgi import form


class Textbox(form.Input):

    def __init__(self, default_text, *boolean_attributes, **attributes):
        super().__init__(
                form.TEXT,
                children=default_text,
                boolean_attributes=boolean_attributes,
                attributes=attributes
                )


class LabeledTextbox(form.Label):

    def __init__(
            self,
            label,
            default_text,
            *boolean_attributes,
            label_attributes={},
            **attributes
            ):
        super().__init__(label, **label_attributes)
        textbox = Textbox(default_text, *boolean_attributes, **attributes)
        self.wrap(textbox)
