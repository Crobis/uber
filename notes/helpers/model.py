import os
import datetime
from uuid import uuid4
from pathlib import Path

from django.utils.translation import get_language
from django.utils.html import strip_tags as st
from django.apps import apps




class PathAndRename:
    def __init__(self, path):
        self.path  = path 

    def wrapper(self, instance, filename):
        m = getattr(instance.content_object, '_image_upload_dir', None)
        if m:
            self.path = m

        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path ,'{}'.format(datetime.datetime.now().strftime("%Y%m")), filename)

def fallback_to_default_language(name, field):
    def getter(self):
        language = get_language()
        deflanguage = settings.LANGUAGE_CODE
        f= to_attribute(name)
        value = getattr(self, f, None)
        if value: 
            return value
        value = getattr(self, '{}_{}'.format(name, deflanguage), '')
        return value
    return getter



def decode_block(block, theme='default'):
    Picture = apps.get_model('notes', 'Picture')
    # print(block)
    if block.type == 'paragraph':
        return '<p>{}</p>'.format(block.data['text'])

        

    elif block.type == 'linkTool':
        if block.data['meta']:
            print(block.data['meta'])
            image = ''
            if 'image' in block.data['meta']:
                if 'id' in block.data['meta']['image']:
                    
                    image = Picture.objects.filter(pk=block.data['meta']['image']['id']).first()
                    if image:
                        image = image.thumbnail_square.url
                else:
                    image = block.data['meta']['image']['url']


            return '''
                <div class="card linktool compact">                   
                    <div class="card-body">
                        <div class="card-image" style="background-image: url('{image}');"></div>
                        <h5 class="card-title">{title}</h5>                    
                        <p class="card-text text-muted">{description}</p>
                        <a href="{url}" class="card-link">{url}</a>                        
                    </div>
                </div>
            '''.format(
                title=st(block.data['meta']['title']),
                description=st(block.data['meta']['description']),
                url=block.data['link'],
                image=image
            )


        else:
            return '''
                <div class="card">
                    <div class="card-body">
                        <a href="{url}" class="card-link">{url}</a>
                    </div>
                </div>
            '''.format(

                url=block.data['link'],
            )
        # return '<p>{}</p>'.format(block.data['link'])

    return ''