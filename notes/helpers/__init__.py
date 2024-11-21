import hashlib
import requests
from PIL import Image

from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.apps import apps

from .model import *



def gen_small_hash(s):
    return hashlib.shake_128(str(s).encode()).hexdigest(4)

def get_image_from_url(img_url):
    try:
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with NamedTemporaryFile() as img_temp:
                img_temp.write(r.content)
                img_temp.flush()                

                img = Image.open(img_temp)
                width, height = img.size

                img = img.convert("RGB") 
                img.save(img_temp.name, "webp", quality=80)
                img_temp.flush()

                image_size = os.path.getsize(img_temp.name)

                file_name = os.path.splitext(os.path.basename(img_url))[0] + '.webp'

                Picture = apps.get_model('notes', 'Picture')
                picture = Picture(
                    type = 'from_url',
                    pic = File(img_temp, name=file_name),
                    original_filename = os.path.basename(img_url),
                    is_tmp = True,
                    size = image_size,
                    width = width,
                    height = height,
                    session_key = 'asd'
                )
                picture.save()

                img_url = picture.pic
                if not picture.pic.path.startswith('/'):
                    img_url = f'/{img_url}'
                    
                return { 'url': img_url, 'id': picture.id }
    except Exception as e:
        print('get_image_from_url error: ', e)

    return None