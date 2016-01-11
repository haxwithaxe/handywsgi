
from ..templator import TemplatingMixin


def bool_to_attribute_pair(boolean, attribute):
    if boolean:
        return '%s="%s"' % (attribute, attribute)
    return ''


def dict_to_attributes(attribute_dict):
    if not attribute_dict:
        return ''
    attributes = []
    for key, value in attribute_dict.items():
        attributes.append('%s="%s"' % (key, value))
    return ' '.join(attributes)


class ButtonGroup(TemplatingMixin):

    def __init__(self, label, *buttons):
        self.label = label
        self.name = "name"
        self.buttons = buttons
        self.fieldset_attributes = {}
        self.label_attributes = {}
        self.group_attributes = {}


    def __dict__(self):
        return {
                'buttons': '\n'.join([str(x) for x in self.buttons]),
                'label': self.label,
                'fieldset_attributes': dict_to_attributes(self.fieldset_attributes),
                'label_attributes': dict_to_attributes(self.label_attributes),
                'group_attributes': dict_to_attributes(self.group_attributes)
                }
        

class Button(TemplatingMixin):

    def __init__(self, name, value, option, selected=False):
        self.name = name
        self.value = value
        self.option = option
        self.selected = selected
        self.attributes = {}
        self.label_attributes = {}

    def __dict__(self):
        return {'name': self.name, 'option': self.option, 'value': self.value,
                'selected': bool_to_attribute_pair(self.selected, 'selected'),
                'attributes': dict_to_attributes(self.attributes),
                'label_attributes': dict_to_attributes(self.label_attributes)
                }
