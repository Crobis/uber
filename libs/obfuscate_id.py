import hashids
from django.conf import settings



hid = hashids.Hashids(**settings.HASHIDS)

def encode_id(_id: int) -> str:    
    return hid.encode(_id)

def decode_id(_id: str) -> int:
    decoded_values = hid.decode(_id)
    if len(decoded_values) != 1:
        raise ValueError
    return decoded_values[0]


class HashidsConverter:
    regex = '[0-9a-zA-Z]+'

    def to_python(self, value: str) -> int:
        return decode_id(value)

    def to_url(self, value: int) -> str:
        return encode_id(value)