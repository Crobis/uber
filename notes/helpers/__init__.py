import hashlib

from .model import *


def gen_small_hash(s):
    return hashlib.shake_128(str(s).encode()).hexdigest(4)

