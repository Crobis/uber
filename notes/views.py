import json
from json.decoder import JSONDecodeError

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q, Count
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from page.context_processors import page_components
from .models import Picture, Note, Tag,  save_info
from .forms import ModifyNote, SearchForm

from core.helpers import is_ajax


@login_required
def index(request):








    form = ModifyNote()

    pictures = Picture.objects.all()


    test = {
        'a': 1,
        'b': 2,
    }

    # a = test['s'] or 'a'

    # print(a)
    

    # print(gen_small_hash(1))
    
    return render(request, 'notes/index.html', {
        'pictures': pictures,
        'form': form,
        'data': data.items()
    }) 


@login_required
def list_notes(request, tag_id = None):
    kwargs = {'archive': False}
    exkwargs = {'tags__title__iexact': 'todo'}
    args = Q()

    if tag_id:
        tag = Tag.objects.get(pk=tag_id)
        kwargs['tags__id__in'] = [tag.id]
        del exkwargs['tags__title__iexact']
    


    G = request.GET.copy()
    search_form = SearchForm(G)
    if search_form.is_valid():
        if search_form.cleaned_data['search']:
            subargs = Q()
            search_fields = ['description__icontains', 'tags__title__icontains']
            for field in search_fields:
                subargs |= Q(**{field: search_form.cleaned_data['search']})

            args &= subargs

    notes = Note.objects.filter(args, **kwargs).exclude(**exkwargs)

    return render(request, 'notes/list_all.html', {
        'notes': notes,
        'search_form': search_form
    }) 



def view_note(request, note_id):
    public_view = False
    # blocks = request.context['blocks'].copy()
    blocks = page_components(request)['blocks'].copy()
    print(blocks)

    if isinstance(note_id, int):
        if not request.user.is_authenticated:
            return redirect('/')
        note = get_object_or_404(Note, pk=note_id)
    else:
        note = get_object_or_404(Note, public_link=note_id)
        public_view = True
        blocks['main'] = 'col-md-12'
        blocks['side'] = 'd-none'

    
    return render(request, 'notes/view.html', {
        'note': note,
        'public_view': public_view,
        'blocks': blocks 
    }) 

@login_required
def modify_note(request, note_id=None):
    tags = ''
    note = None
    if note_id:
        note = Note.objects.get(pk=note_id)
        tags = note.load_tags('json')

    P = request.POST.copy()

    if P:
        form = ModifyNote(P, instance=note)
        if form.is_valid():
            note = form.save()
            save_info(note, request)
            tags = form.cleaned_data['tags']

            try:
                tags = json.loads(tags)
            except JSONDecodeError as e:
                tags = []

            tags_from_post = []
            for tag in tags:
                tag_object, created = Tag.objects.get_or_create(
                    title=tag['value'],
                )
                tags_from_post.append(tag_object)
                save_info(tag_object, request)            

            note.tags.add(*tags_from_post)
            for tag in note.tags.all():
                if tag not in tags_from_post:
                    note.tags.remove(tag)

            return redirect(reverse('notes:view_note', kwargs={'note_id': note.id} ))

    else:
        form = ModifyNote(instance=note, initial={'tags': tags})



    return render(request, 'notes/add.html', {
        'form': form,
    }) 


@login_required
def delete_note(request, note_id=None):
    note = get_object_or_404(Note, pk=note_id)
    note.archive = True
    note.save()
    return redirect(reverse('notes:list_notes'))


@login_required
def list_tags(request):

    if is_ajax(request):
        data = json.loads(request.body)
        query = data.get('query', '')
        tags = Tag.objects.filter(title__icontains=query, note__archive=False).values_list('title', flat=True)
        return JsonResponse(list(tags), safe=False)


    tags = Tag.objects.all() \
                .annotate(notes_count=Count('note', filter=Q(note__archive=False))) \
                .filter(notes_count__gt=0) \
                .order_by('-notes_count')



    return render(request, 'tags/list_all.html', {
        'tags': tags,
    }) 

