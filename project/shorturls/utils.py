import struct

from django.core.signing import b64_encode, b64_decode
from django.utils.encoding import smart_str


def token_encode(content_type_id, object_id):
    """
    Encodes the content_type_id and object_id values into a packed string.
    """
    data = struct.pack('!QQ', content_type_id, object_id)

    # Set content_type_id and object_id
    content_type_id = data[:8].lstrip('\0')
    object_id = data[8:].lstrip('\0')

    # Set the size of our values
    size = struct.pack('!B', len(content_type_id) << 4 | len(object_id))

    return b64_encode(size + content_type_id + object_id)


def token_decode(token):
    """
    Extracts the content_type_id and object_id values from the packed string.
    """
    data = b64_decode(smart_str(token))

    # Get the sizes of our values
    offset = 0
    format = '!B'

    (size,) = struct.unpack_from(format, data, offset)

    type_len = (size & 0b11110000) >> 4
    obj_len = (size & 0b00001111)

    # Get content_type_id and object_id
    offset += struct.calcsize(format)
    format = '!%ds%ds' % (type_len, obj_len)

    content_type_id, object_id = struct.unpack_from(format, data, offset)

    # Add pad bytes and unpack ``unsigned long long`` values
    content_type_id, object_id = struct.unpack('!QQ', '%s%s' % (
        content_type_id.rjust(8, '\0'), object_id.rjust(8, '\0')
    ))

    return content_type_id, object_id
