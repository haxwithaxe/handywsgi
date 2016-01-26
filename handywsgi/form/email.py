
from handywsgi import form


class Email(form.Input):

    def __init__(self, default_text, *boolean_attributes, **attributes):
        super().__init__(form.EMAIL, children=default_text, boolean_attributes=boolean_attributes, attributes=attributes)


class LabeledEmail(form.Label):

    def __init__(self, label, default_text, *boolean_attributes, label_attributes={}, **attributes):
        super().__init__(label, **label_attributes)
        email = Email(default_text, *boolean_attributes, **attributes)
        self.wrap(email)
