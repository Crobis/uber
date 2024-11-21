import os
import json
import pprint
import requests
import tempfile
from json.decoder import JSONDecodeError

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q, Count
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required


from linkpreview import link_preview
from linkpreview import Link, LinkPreview, LinkGrabber


from page.context_processors import page_components
from .models import Picture, Note, Block, Tag, save_info
from .forms import ModifyNote, SearchForm

from core.helpers import is_ajax, is_integer
from .helpers import get_image_from_url


pp = pprint.PrettyPrinter(indent=0,  width=120)

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





def service_endpoint(request, service_type):
    response = {'status': 'OK'}


    if service_type == 'get_url':
        response = { 'success' : 0 }
        url = request.GET.get('url')
        if url:

            try:
                grabber = LinkGrabber(
                    initial_timeout=20,
                    maxsize=10485760,
                    receive_timeout=10,
                    chunk_size=1024,
                )
                content, url = grabber.get_content(url)
                link = Link(url, content)
                preview = LinkPreview(link)

                favicons = getattr(preview, 'favicon', [])
                favicon = None
                for fi in favicons:
                    favicon = fi[0]
                    break

                meta = {
                    'title': getattr(preview, 'title', None),
                    'description': getattr(preview, 'description', None),
                    'image': getattr(preview, 'image', None),
                    'site_name': getattr(preview, 'site_name', None),
                    'favicon': favicon,
                }

                if getattr(preview, 'absolute_image', None):
                    meta['image'] = {
                        'url':  getattr(preview, 'absolute_image', None)
                    }
                
                if meta['image'] and meta['image']['url']:
                    img_url = get_image_from_url(meta['image']['url'])
                    if img_url:
                        meta['image'] = img_url
                
                if meta['favicon']:
                    img_url = get_image_from_url(meta['favicon'])
                    if img_url:
                        meta['favicon']= img_url

                response['success'] = 1
                response['meta'] = meta
                # pp.pprint(meta)               
            except Exception as e:
                response['erros'] = e
                print(f'Cant get url: {url} - {e}')






    return JsonResponse(response)



@login_required
def modify_note(request, note_id=None):
    tags = ''
    note = None
    if note_id:
        note = Note.objects.get(pk=note_id)
        tags = note.load_tags('json')

    # print('request.headers', request.headers)
    # print('is_ajax', is_ajax(request))



    if is_ajax(request):
        data = json.loads(request.body)
        # print('data', data)
        pp = pprint.PrettyPrinter(indent=0,  width=120)
        pp.pprint(data)

        action = data.get('action')

        if action == 'save':

            blocks = data.get('blocks',[])

            if len(blocks) > 0 and not note:
                note = Note()
                note.save()
                data['redirect'] = reverse('notes:edit_note', kwargs={'note_id': note.id} )

            used_ids = []
            for i, block in enumerate(blocks):
                
                if is_integer(block['id']):
                    b = Block.objects.get(note=note, id=block['id'])
                else:
                    b = Block(type = block['type'], note = note)

                b.type = block['type']
                b.data = block['data']
                b.order = i
                b.save()

                save_info(b, request)
                used_ids.append(b.id)

            for block in Block.objects.filter(note=note).exclude(id__in=used_ids):
                block.delete()

            save_info(note, request) 
                



            pass 
        elif action == 'load':
            data =         {
                "time": 1732051259177,
                "blocks": [
                {"id": 1, "type": "paragraph", "data": {"text": "asdasdasd"}},
                {"id": 2, "type": "paragraph", "data": {"text": "asdasd"}},
                {"id": 3, "type": "header", "data": {"text": "asddasd", "level": 2}}
                ],
                "version": "2.30.7"
            }

        return JsonResponse(data)
        






    # P = request.POST.copy()

    # if P:
    #     form = ModifyNote(P, instance=note)
    #     if form.is_valid():
    #         note = form.save()
    #         save_info(note, request)
    #         tags = form.cleaned_data['tags']

    #         try:
    #             tags = json.loads(tags)
    #         except JSONDecodeError as e:
    #             tags = []

    #         tags_from_post = []
    #         for tag in tags:
    #             tag_object, created = Tag.objects.get_or_create(
    #                 title=tag['value'],
    #             )
    #             tags_from_post.append(tag_object)
    #             save_info(tag_object, request)            

    #         note.tags.add(*tags_from_post)
    #         for tag in note.tags.all():
    #             if tag not in tags_from_post:
    #                 note.tags.remove(tag)

    #         return redirect(reverse('notes:view_note', kwargs={'note_id': note.id} ))

    # else:
    #     form = ModifyNote(instance=note, initial={'tags': tags})

    editor_data = {}
    if note:
        editor_data = note.get_data_for_editor()


    return render(request, 'notes/add.html', {
        'note': note,
        'editor_data': editor_data
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

