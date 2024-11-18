import random
import string



def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def is_htmx(request):
    return True if request.META.get('HTTP_HX_REQUEST') else False

def random_string(size=6, chars=string.ascii_lowercase +string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



