
from handywsgi import form


class Radio(form.Input):

    def __init__(self, label, *boolean_attributes, **attributes):
        super().__init__(form.RADIO, children=label, boolean_attributes=boolean_attributes, attributes=attributes)


class LabeledRadio(form.Label):

    def __init__(self, label, *boolean_attributes, label_attributes=None, **attributes):
        super().__init__(label, **(label_attributes or {}))
        radio = Radio(*boolean_attributes, **attributes)
        self.wrap(radio)
