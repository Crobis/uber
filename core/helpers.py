import random
import string



def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def is_htmx(request):
    return True if request.META.get('HTTP_HX_REQUEST') else False

def random_string(size=6, chars=string.ascii_lowercase +string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def is_integer(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False

def getattrd(dictionary, keys, default=None):
    for key in keys.split('.'):
        if isinstance(dictionary, dict):
            dictionary = dictionary.get(key, default)
        elif isinstance(dictionary, list) and isinstance(key, int):
            if 0 <= key < len(dictionary):
                dictionary = dictionary[key]
            else:
                return default
        else:
            return default
    return dictionary