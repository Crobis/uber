import os
import datetime
from uuid import uuid4
from pathlib import Path

from django.utils.translation import get_language


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
