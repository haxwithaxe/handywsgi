
from handywsgi import form


class Checkbox(form.Input):

    def __init__(self, label, value, flags=None, attributes=None, **kwargs):
        super().__init__(
                form.CHECKBOX,
                children=label,
                flags=flags,
                attributes=attributes,
                **kwargs
                )
        self.attributes.update({'value': value})


class LabeledCheckbox(form.Label):

        child_tag = Checkbox


class CheckboxGroup(form.BaseGroup):
    
    plain_type = Checkbox
    labeled_type = LabeledCheckbox
