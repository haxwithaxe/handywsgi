
import io
import collections
import threading


def file_io(filename):
    """ Returns a function that returns a FileIO instance with ``filename`` as the target. 
    
    This is an interface adapter so that the FileIO class can be used interchangeably with IOBuffer.
    
    """
    return lambda: FileIO(filename)




class IOBuffer:
    """ A bytes vs str input agnostic read-write buffer implementation.

    This is a [https://docs.python.org/3/library/io.html|file-like] class.
    
    Attributes:
        encoding (str): Encoding of the text stream.
        errors: The error setting of the decoder or encoder.
        mode (str): The mode as given in the constructor.
        name (str): The file name. This is the file descriptor of the file when no name is given in the constructor.
        closed (bool): True if the stream is closed.


    Args:
        data (str or bytes): Seed for the buffer.
        encoding (str): If str output is desired this will be used to translate to and from bytes. Defaults to ``utf-8``.
        buffer_class: A file-like class to be used as a buffer.

    """

    def __init__(self, data=None, encoding='utf-8', buffer_class=None):
        self._buffer = io.BytesIO()
        self.encoding = encoding
        if data:
            self.write(data)

    @property
    def closed(self):
        return self._buffer.closed

    def use_buffer(self, buffer_object):
        self._buffer = buffer_object

    def write(self, data):
        """ Write a string (str or bytes) to the buffer. """
        data_bytes = self.to_bytes(data)
        self._buffer.write(data_bytes)

    def writeln(self, line=''):
        """ Write a string to the buffer with an appended newline. """
        return self.write(line+'\n')

    def read(self, count=-1):
        """ Read at most ``count`` characters from stream.

        Read from underlying buffer until we have ``count`` characters or
        we hit EOF. If ``count`` is negative or omitted, read until EOF.

        """
        return self.from_bytes(self.read_bytes(count))

    def read_bytes(self, count=-1):
        """ Read at most ``count`` bytes from the buffer.

        Read from underlying buffer until we have ``count`` bytes or
        we hit EOF.
        If ``count`` is negative or omitted, read until EOF.

        """
        self._buffer.seek(0, 0)
        data = self._buffer.read(count)
        self._pos = self._buffer.tell()
        self._buffer.seek(0, 2)
        return data

    def seek(self, offset, whence=0):
        """ Change stream position.
      
        Change the stream position to the given byte offset.

        offset (int): interpreted relative to the position indicated by ``whence``.
        whence (int): Defaults to 0.      
            * 0 -- start of stream (the default); offset should be zero or positive
            * 1 -- current stream position; offset may be negative
            * 2 -- end of stream; offset is usually negative

        Returns:
            int: The new absolute position.

        """
        return self._buffer.seek(offset, whence)

    def tell(self):
        return self._buffer.tell()

    def readline(self, line_size=-1):
        """ Read until newline or EOF.

        Args:
            line_size (int): The size of a line in number of bytes. Values of 0 or less will not force the line length.

        Returns:
            str: A line or an empty string if EOF is hit immediately.
        
        """
        line = self._buffer.readline(line_size)
        return self.decode(line)


    def readlines(self, line_size=-1):
        """ Read and return a list of lines from the stream.

        Args:
            line_size: The number of bytes in a line.

        Returns:
            list: A list of lines from the stream. If ``encoding`` is set in this instance the list will returns strings
                otherwise it will contain bytes.

        """
        lines = self._buffer.readlines(line_size)
        for line in lines:
            yield self.from_bytes(line)

    def writelines(self, lines):
        """ Write a list of lines to the buffer.
        
        Uses ``self.encoding`` if ``lines`` is a list of ``str``.

        Line separators are not added, so it is usual for each of the lines provided to have a line separator at the end.

        """
        for line in lines:
            self.write(line)

    def close(self):
        self._buffer.close()

    def prepend(self, other):
        """ Prepend the content of this buffer to another buffer.

        Returns:
            object: The buffer passed to this method.

        """
        other.write(self.read_bytes())
        return other

    def flush(self):
        """ Does nothing. """
        self._buffer.flush()

    def encode(self, text, encoding=None):
        if encoding or self.encoding:
            return text.encode(encoding=encoding or self.encoding)
        return text

    def decode(self, data, encoding=None):
        if encoding or self.encoding:
            return data.decode(encoding=encoding or self.encoding)
        return data

    def __len__(self):
        pos = self._buffer.tell()
        length = self._buffer.seek(0, 2)
        self._buffer.seek(pos)
        return length

    def __iter__(self):
        return self

    def __next__(self):
        line = self._buffer.readline()
        if line == -1:
            raise StopIteration()
        return line

    def __del__(self):
        if hasattr(self, 'buffer'):
            del self._buffer

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def to_bytes(self, data):
        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            encoded = self.encode(data)
            return encoded

    def from_bytes(self, data):
        if self.encoding:
            return self.decode(data)
        else:
            return data

    def isatty(self):
        """ Return whether this is an 'interactive' stream.

        Return False if it can't be determined.

        """
        return False

    def readable(self):
        """ Return whether object was opened for reading.
        
        Always returns True.
        
        """
        return True

    def writable(self):
        """ Return whether object was opened for writing.
        
        Always returns True.
        
        """
        return True


class FileIO:
    """ A read-write implementation of a file object.

    Attributes:
        name (str): The filename.

    Note:
        May contain threadsafety.

    """

    def __init__(self, filename):
        self._filename = filename
        self._pos = 0
        self._lock = threading.Lock()

    @property
    def name(self):
        return self._filename

    def read(self, size=-1):
        """ Read bytes from the file on disk. """
        return self._read_operation('read', size=size)

    def readline(self, size=-1):
        """ Read a line of bytes terminated with b'\n', all bytes until EOF or, ``size`` bytes from the file on disk. """
        return self._read_operation('readline', size=size)

    def readlines(self, size=-1):
        """ Return the output of readline() until EOF or ``size`` lines is reached. """
        return self._read_operation('readline', size=size)

    def write(self, data):
        """ Write bytes ``data`` to disk.
        
        Returns:
            int: The number of bytes written.

        """
        return self._write_operation('write', data)

    def writelines(self, lines):
        """ Write a list of byte arrarys to disk. """
        return self._write_operation('writelines', lines)

    def _read_operation(self, operation, *args, **kwargs):
        """ A generic abstraction of all read operations enabling locking. """
        self.lock()
        with open(self._filename, 'rb') as source:
            source.seek(self._pos)
            data = getattr(source, operation)(*args, **kwargs)
            self._pos = source.tell()
        self.unlock()
        return data

    def _write_operation(self, operation, *args, **kwargs):
        """ A generic abstraction of all write operations enabling locking. """
        self.lock()
        with open(self._filename, 'ab') as sink:
            sink.seek(self._pos)
            bytes_written = getattr(sink, operation)(*args, **kwargs)
            self._pos = sink.tell()
        self.unlock()
        return bytes_written

    def lock(self):
        """ Prevent simultaneous read and write operations. """
        self._lock.aquire()

    def unlock(self):
        """ Prevent simultaneous read and write operations. """
        self._lock.release()

    def seek(self, offset, whence=0):
        """ Change the stream position to the given byte offset.

        offset is interpreted relative to the position indicated by whence. The
        default value for whence is 0.

        Values for whence are:

            0 – Start of the stream (the default); offset should be zero or positive.
            1 – Current stream position; offset may be negative.
            2 – End of the stream; offset is usually negative.

        Returns:
            The new absolute position.

        """
        if whence == 1:
            self._pos += offset
        elif whence == 2:
            self._pos = -abs(offset)
        else:
            self._pos = offset
        return self._pos

    def tell(self):
        """ Returns the current file position. """
        return self._pos
