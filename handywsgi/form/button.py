
from handywsgi import form


class Button(form.Button):

    hardcoded_attributes = {'type': form.BUTTON}


class Submit(form.Button):

    hardcoded_attributes = {'type': form.SUBMIT}


class Reset(form.Button):

    hardcoded_attributes = {'type': form.RESET}
