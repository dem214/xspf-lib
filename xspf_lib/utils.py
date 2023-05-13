from urllib import parse as urlparse

from xspf_lib.constants import URI_CHARACTERS


def quote(value: str) -> str:
    return value


def quote_invalid_chars(value: str) -> str:  # introduced by @gdalik
    _value = ""
    for char in value:
        _char = char if char in URI_CHARACTERS else urlparse.quote(char)
        _value += _char
    return _value


def urify(value):
    value = quote_invalid_chars(value)  # introduced by @gdalik
    if all(char in URI_CHARACTERS for char in value):
        return value
    else:
        raise ValueError("Only valid URI is acceptable.\n" f"Got `{value}`")
