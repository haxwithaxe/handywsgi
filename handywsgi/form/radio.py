
from handywsgi import form


class Radio(form.Input):

    hardcoded_attributes = {form.TYPE: form.RADIO}


class LabeledRadio(form.Label):

    hardcoded_attributes = {form.TYPE: form.RADIO}
    child_tag = Radio


class RadioGroup(form.FieldSet):

    plain_type = Radio
    labeled_type = LabeledRadio
