
from . import ButtonGroup, Button


class Group(ButtonGroup):

    template = '''
        <fieldset $fieldset_attributes>
            <legend $label_attributes>$label</legend>
            $buttons
        </fieldset>
        '''


class Radio(Button):

    template = '''
        <label $label_attributes>
            <input type="radio" name="$name" value="$value" $attributes />
        </label>
        '''
