
from handywsgi import form


class Checkbox(form.Input):

    def __init__(self, label, value, *boolean_attributes, **attributes):
        attributes['value'] = value
        super().__init__(
                form.CHECKBOX,
                children=label,
                boolean_attributes=boolean_attributes,
                attributes=attributes
                )


class LabeledCheckbox(form.Label):

    def __init__(
            self,
            label,
            *boolean_attributes,
            label_attributes={},
            **attributes
            ):
        super().__init__(label, **label_attributes)
        checkbox = Checkbox(*boolean_attributes, **attributes)
        self.wrap(checkbox)


class CheckboxGroup:

    def __init__(self, options, legend=None, labeled=False):
        self._legend = legend
        if labeled:
            checkbox_class = LabeledCheckbox
        else:
            checkbox_class = Checkbox
        self._options = []
        for option in options:
            self._options.append(checkbox_class(**option))

    def __str__(self):
        if self._legend:
            self._options.insert(0, form.make_tag(form.LEGEND, self._legend))
        return '\n'.join((str(x) for x in self._options))
