
from handywsgi import form


class Textbox(form.Input):
    """ Input element of type ``text``.
    
    Arguments:
        default_text (str, optional): Default text displayed in the textbox.
        flags (tuple, optional): `tuple` of strings representing html element flag attributes.

    Keyword Arguments:
        attributes: HTML element attributes.

    Example:
        >>> my_textbox = Textbox('Your name here.', 'disabled', class_='form-input', name='username')
        >>> str(my_textbox)
        '<input type="text" name="username" class="my-class" value="Your name here."/>'

    """

    def __init__(self, default_text=None, flags=None, attributes=None, **kwargs):
        super().__init__(
                form.TEXT,
                children=default_text,
                flags=flags,
                attributes=attributes,
                **kwargs
                )


class LabeledTextbox(form.Label):
    """ Labeled input element of type ``text``.
    
    Arguments:
        label (str): A string to use as the label text.
        default_text (str, optional): Default text displayed in the textbox.
        flags (tuple or str, optional): `tuple` of strings representing html element flag attributes.
        label_flags (tuple or str, optional): `tuple` of strings representing html element flag attributes for the label.
        attributes (dict, optional): HTML element attributes.
        label_attributes (dict, optional): HTML element attributes for the label.

    Example:
        >>> my_labeled_textbox = LabeledTextbox(
                'label text',
                default_text='Your name here.',
                flags='disabled',
                label_flags='fake-flag',
                attributes={'class_': 'form-input', 'name': 'username'},
                label_attributes={'class': 'shiny-label'}
                )
        >>> str(my_labeled_textbox)
        '''
        <label fake-flag="fake-flag" class="shiny-label">
            label text
            <input type="text" name="username" class="my-class" value="Your name here." />
        </label>
        '''

    """

    child_tag = Textbox
