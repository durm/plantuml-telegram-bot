import zlib
import re


DIAGRAM = re.compile("(?P<full>@startuml\n(.+(\n)*)+@enduml)")


def deflate_and_encode(plantuml_text):
    zlibbed_str = zlib.compress(plantuml_text)
    compressed_string = zlibbed_str[2:-4]
    return encode(compressed_string)


def encode(data):
    res = ""
    for i in range(0, len(data), 3):
        if i + 2 == len(data):
            res += _encode3bytes(data[i], data[i + 1], 0)
        elif i + 1 == len(data):
            res += _encode3bytes(data[i], 0, 0)
        else:
            res += _encode3bytes(data[i], data[i + 1], data[i + 2])
    return res


def _encode3bytes(b1, b2, b3):
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    res = ""
    res += _encode6bit(c1 & 0x3F)
    res += _encode6bit(c2 & 0x3F)
    res += _encode6bit(c3 & 0x3F)
    res += _encode6bit(c4 & 0x3F)
    return res


def _encode6bit(b):
    if b < 10:
        return chr(48 + b)
    b -= 10
    if b < 26:
        return chr(65 + b)
    b -= 26
    if b < 26:
        return chr(97 + b)
    b -= 26
    if b == 0:
        return '-'
    if b == 1:
        return '_'
    return '?'


def get_uml(message):
    match = DIAGRAM.search(message)
    if match:
        return match.groupdict()['full']