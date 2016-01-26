
from handywsgi import form


class Submit(form.Button):

    def __init__(self, title, *boolean_attributes, **attributes):
        super().__init__(title, *boolean_attributes, type_=form.SUBMIT, **attributes)


class Reset(form.Button):

    def __init__(self, title, *boolean_attributes, **attributes):
        super().__init__(form.RESET, title, boolean_attributes=boolean_attributes, attributes=attributes)
