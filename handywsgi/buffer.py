
import io
import threading


def file_io(filename):
    return lambda: FileIO(filename)


class IOBuffer:
    """ A bytes vs str input agnostic buffer implementation. """

    def __init__(self, data=None, encoding='utf-8', buffer_class=None):
        self._buffer = io.BytesIO()
        self._encoding = encoding
        if data:
            self.write(data)

    @property
    def closed(self):
        return self._buffer.closed

    def use_buffer(self, buffer_object):
        self._buffer = buffer_object


    def write(self, data):
        """ Write a string (str or bytes) to the buffer. """
        if isinstance(data, bytes):
            self._buffer.write(data)
        elif isinstance(data, str):
            encoded = self._encode(data)
            self._buffer.write(encoded)

    def writeln(self, line):
        """ Write a string to the buffer with an appended newline. """
        return self.write(line+'\n')

    def read(self, count=-1):
        data = self.read_bytes(count)
        return self._decode(data)

    def read_bytes(self, count=-1):
        self._buffer.seek(0, 0)
        data = self._buffer.read(count)
        self._buffer.seek(0, 2)
        return data

    def seek(self, offset, whence=0):
        return self._buffer.seek(offset, whence)

    def tell(self):
        return self._buffer.tell()

    def readline(self, size=-1):
        line = self._buffer.readline(size)
        return self._decode(line)

    def readlines(self, hint=-1):
        """ Read and return a list of lines from the stream.

        Args:
            hint can be specified to control the number of lines read:
                no more lines will be read if the total size (in bytes/characters) of all lines so far exceeds hint.

        """
        lines = self._buffer.readlines(hint)
        if self._encoding:
            for line in lines:
                yield self._decode(line)
        else:
            return lines

    def writelines(self, lines):
        """ Write a list of lines to the stream using the encoding set in __init__ if ``lines`` is a list of ``str``.

        Line separators are not added, so it is usual for each of the lines provided to have a line separator at the end.

        """
        for line in lines:
            self.write(line)

    def close(self):
        self._buffer.close()

    def prepend(self, other):
        other.write(self.read_bytes())
        return other

    def _encode(self, text, encoding=None):
        if encoding or self._encoding:
            return text.encode(encoding=encoding or self._encoding)
        return text

    def _decode(self, data, encoding=None):
        if encoding or self._encoding:
            return data.decode(encoding=encoding or self._encoding)
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
        if hasattr(self, '_buffer'):
            del self._buffer

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class FileIO:
    """ A read-write implementation of a file object.
    
    Note:
        May contain threadsafety.

    """

    def __init__(self, filename):
        self._filename = filename
        self._pos = 0
        self._lock = threading.Lock()

    def read(self, size=-1):
        return self._read_operation('read', size=size)

    def readline(self, size=-1):
        return self._read_operation('readline', size=size)

    def readlines(self, hint=-1):
        return self._read_operation('readline', size=size)

    def write(self, data):
        return self._write_operation('write', data)

    def writelines(self, lines):
        return self._write_operation('writelines', lines)

    def _read_operation(self, operation, *args, **kwargs):
        self.lock()
        with open(self._filename, 'rb') as source:
            source.seek(self._pos)
            data = getattr(source, operation)(*args, **kwargs)
            self._pos = source.tell()
        self.unlock()
        return data

    def _write_operation(self, operation, *args, **kwargs):
        self.lock()
        with open(self._filename, 'ab') as sink:
            sink.seek(self._pos)
            bytes_written = getattr(sink, operation)(*args, **kwargs)
            self._pos = sink.tell()
        self.unlock()
        return bytes_written

    def lock(self):
        self._lock.aquire()

    def unlock(self):
        self._lock.release()

    def seek(self, offset, whence=0):
        """ 
        excerpt from python docs:
            seek(offset[, whence])

                Change the stream position to the given byte offset. offset is interpreted relative to the position indicated by whence. The default value for whence is SEEK_SET. Values for whence are:

                    SEEK_SET or 0 – start of the stream (the default); offset should be zero or positive
                    SEEK_CUR or 1 – current stream position; offset may be negative
                    SEEK_END or 2 – end of the stream; offset is usually negative

            Return the new absolute position.

        """
        if whence == 1:
            pos = self._pos + offset
        if whence == 2:
            pos = -abs(offset)
        self._pos = offset
        return self._pos

    def tell(self):
        return self._pos
