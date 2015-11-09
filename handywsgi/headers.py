

def _validate(value):
    """ Protect against HTTP response splitting attack. """
    if '\n' in value or '\r' in value:
        raise ValueError('Invalid characters in header')


class Header:
    """ HTTP Header for WSGI """

    def __init__(self, key, value, unique=False):
        self._key = None
        self.key = key
        self._value = None
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

    def __iter__(self):
        return tuple(self.key, self.value)

    def __str__(self):
        return '{key}: {value}'.format(key=self.key, value=self.value)


class Headers:
    """ HTTP Headers for WSGI """

    def __init__(self, headers=None):
        self._headers = headers or []

    def __getitem__(self, key):
        return (header for header in self._headers if header.key == key)

    def keys(self):
        return (header.key for header in self._headers)

    def add(self, key, value, unique=False):
        header = Header(key, value, unique)
        if unique and header in self._headers:
            matching = [x for x in self._headers if x == header]
            hdr = matching.pop()
            hdr.value = header.value
            # remove duplicates
            for x in matching:
                self._headers.pop(self._headers.index(x))
        else:
            self._headers.append(Header(key, value, unique))

    def to_list(self):
        return [iter(x) for x in self._headers]

    def __str__(self):
        return '\n'.join([str(x) for x in self._headers])+'\n'


