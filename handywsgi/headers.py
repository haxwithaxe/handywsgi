""" Header management tools. """


def _validate(value):
    """ Protect against HTTP response splitting attack. """
    if '\n' in value or '\r' in value:
        raise ValueError('Invalid characters in header')


class Header:
    """ HTTP Header for WSGI

    Keys and values are checked for newlines and a ValueError is raised if any
    are found.

    Args:
        key (str): HTTP Header name.
        value (str): HTTP Header value.
        unique (bool): Marker for enforcing uniqueness. True to enforce
            uniqueness on a FIFO basis.

    """

    def __init__(self, key, value, unique=False):
        self._key = None
        self._value = None
        self.key = key
        self.value = value
        self.unique = unique

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        _validate(key)
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        _validate(value)
        self._value = value

    def __eq__(self, other):
        if self.unique or other.unique:
            return self.key.lower() == other.key.lower()
        return self.key.lower() == other.key.lower() and self.value == other.value

    def __str__(self):
        return '{key}: {value}'.format(key=self.key, value=self.value)


class Headers:
    """ HTTP Headers for WSGI """

    def __init__(self, headers=None):
        self._headers = headers or []

    def __getitem__(self, key):
        """ Get all headers with header.key == key. """
        return (header for header in self._headers if header.key == key)

    def keys(self):
        """ Returns a list of header keys in this instance. """
        return (header.key for header in self._headers)

    def add(self, key, value, unique=False):
        """ Add a header to this instance based on the values passed.

        Args:
            key (str): HTTP Header name.
            value (str): HTTP Header value.
            unique (bool): Marker for enforcing uniqueness. True to enforce
                uniqueness on a FIFO basis.

        """
        header = Header(key, value, unique)
        if unique and header in self._headers:
            matching = [x for x in self._headers if x == header]
            hdr = matching.pop()
            hdr.value = header.value
            # remove duplicates
            for matching_header in matching:
                self._headers.pop(self._headers.index(matching_header))
        else:
            self._headers.append(Header(key, value, unique))

    def items(self):
        """ Return these headers as a list of tuples.

        This is required by the WSGI interface.
        
        """
        return [(x.key, x.value) for x in self._headers]

    def __str__(self):
        return '\n'.join([str(x) for x in self._headers])+'\n'


