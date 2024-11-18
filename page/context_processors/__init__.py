from page.utils import build_top_menu
from notes.models import Note

def page_components(request):


    return {
        'todos' : Note.objects.filter(tags__title__iexact='todo'),
        'top_menu': build_top_menu(request),
        'blocks': {
            'main': 'col-md-8',
            'side': 'col-md-4'
        }
    }


