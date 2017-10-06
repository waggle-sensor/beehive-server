import binascii
import re


def normalize_key(k):
    return re.sub('[-_ ]+', '_', k).lower()


def normalize_value(v):
    if isinstance(v, dict):
        return {normalize_key(k2): normalize_value(v2) for k2, v2 in v.items()}
    if isinstance(v, list):
        return [normalize_value(v2) for v2 in v]
    if isinstance(v, float):
        return round(v, 3)
    return v


def trim_python_repr(s):
    if s.startswith("b'"):
        return s[2:-1]
    return s


def trim_coresense_packet(source):
    start = source.index(b'\xaa')
    end = source.rindex(b'\x55')
    return source[start:end+1]


def reunpack_if_needed(source):
    if source[0] != 0xaa:
        return binascii.unhexlify(source.decode())
    return source


def decode_coresense_3(source):
    from waggle.coresense.utils import decode_frame
    source = trim_coresense_packet(source)
    source = reunpack_if_needed(source)
    return decode_frame(source)


def decode_alphasense_1(source):
    from alphasense.opc import decode18
    return decode18(source)


decoders = {
    'coresense:3': decode_coresense_3,
    'alphasense:1': decode_alphasense_1,
}


def decode(row):
    plugin = ':'.join([row.plugin_name, row.plugin_version])

    source = binascii.unhexlify(trim_python_repr(row.data))

    if plugin not in decoders:
        return {}

    return decoders[plugin](source)
