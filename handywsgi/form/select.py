
from . import bool_to_attribute_pair, ButtonGroup, Button
from ..templator import TemplatingMixin


class Group(ButtonGroup):

    template = '''
        <fieldset $fieldset_attributes>
            <label $label_attributes>$label
                <select $group_attibutes name="$name">
                    $buttons
                </select>
            </label>
        </fieldset>
        '''


class Option(Button):

    template = '''<option $attributes value="$option">$option</option>'''
