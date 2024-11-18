

import os
import datetime
import shutil
import markdown
import json
from pathlib import Path

from django.db import models
from django.utils.translation import get_language, gettext as _
from django.utils.deconstruct import deconstructible
from django.conf import settings
from django.apps import apps
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models.fields.files import ImageFileDescriptor
from django.urls import reverse_lazy, reverse

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from page.models import User

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, SmartCrop, ResizeToFit
from translated_fields import TranslatedField


from .helpers import PathAndRename, fallback_to_default_language


def save_info(obj, request):
    now = datetime.datetime.now()
    user = None

    if not request.user.is_anonymous:
        user = request.user

    if not obj.info:
        info = Info(
            date_created = now,
            date_modified = now,
            user_created = user,
            user_modified = user
        )
        info.save()
        obj.info = info
        obj.save()
    else:
        obj.info.date_modified = now
        obj.info.user_modified = user
        obj.save()

class Note(models.Model):
    title               = models.CharField(_('Title'),max_length=250, blank=True)    
    description         = models.TextField(_('Description'), blank=True, null=True)    
    archive             = models.BooleanField(_('Archive'), default=False)
    tags                = models.ManyToManyField('Tag')
    public_link         = models.SlugField('Public Url', blank=True, null=True, unique=True)

    info                = models.ForeignKey('Info', on_delete=models.CASCADE, blank=True, null=True)



    def save(self, *args, **kwargs):
        if self.description:
            lines = self.description.splitlines()

            for i, line in enumerate(lines):
                if line.startswith("## "):
                    self.title = line.lstrip('## ')
                    break 

        super().save(*args,**kwargs)


    def get_html(self):
        # Split the text into lines
        lines = self.description.splitlines()

        for i, line in enumerate(lines):
            if line.startswith("## "):
                del lines[i]
                # lines[i] = '## [{title}]({url})'.format(
                #     url = reverse('notes:view_note', kwargs={'note_id': self.id} ),
                #     title = line.lstrip('## ')
                # )
                break  

        description = "\n".join(lines)

        md = markdown.Markdown(extensions=["fenced_code", "markdown_checklist.extension"])
        return md.convert(description)

    def load_tags(self, return_format=None):
        tags = []
        if return_format == 'json':
            for tag in self.tags.all():
                tags.append({'value': tag.title})
            return json.dumps(tags)
        return self.tags.all()




    class Meta:
        ordering = ('-id',)





class Tag(models.Model):
    title               = models.CharField(_('Title'),max_length=250, blank=True)    
    archive             = models.BooleanField(_('Archive'), default=False)

    info                = models.ForeignKey('Info', on_delete=models.CASCADE, blank=True, null=True)

    def get_html(self):
        md = markdown.Markdown(extensions=["fenced_code"])
        return md.convert(self.description)

    class Meta:
        ordering = ('-id',)


class Info(models.Model):
    date_created        = models.DateTimeField(_('Izveidots'), auto_now_add=True, blank=True)
    date_modified       = models.DateTimeField(_('Labots'), auto_now=True, blank=True)
    user_created        = models.ForeignKey(User,verbose_name=_('Lietotājs izveidoja'),blank=True, null=True,related_name="user_created_note", on_delete=models.CASCADE)
    user_modified       = models.ForeignKey(User,verbose_name=_('Lietotājs laboja'),blank=True, null=True,related_name="user_modified_note", on_delete=models.CASCADE)




class Picture(models.Model):
    # default upload directory
    path_and_rename     = PathAndRename('uploads/images/').wrapper
    # upload directory for this model whan attached through content_object
    _image_upload_dir   = 'uploads/picture_images/'


    pic                 = models.ImageField(upload_to=path_and_rename)
    original_filename   = models.CharField(_('Original filename'), max_length=250, blank=True)

    title               = models.CharField(_('Title'),max_length=250, blank=True)
    description         = models.TextField(_('Description'), blank=True)

    content_type        = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id           = models.PositiveIntegerField()
    content_object      = GenericForeignKey('content_type', 'object_id')

    thumbnail           = ImageSpecField(source='pic', processors=[ResizeToFill(620, 490)], format='webp', options={'quality': 80} )
    thumbnail_square    = ImageSpecField(source='pic', processors=[ResizeToFill(200, 200)], format='webp', options={'quality': 80} )
    big_view            = ImageSpecField(source='pic', processors=[ResizeToFit(2048,1363)], format='webp', options={'quality': 80} )
    small_view          = ImageSpecField(source='pic', processors=[ResizeToFill(1024, 681)], format='webp', options={'quality': 80} )

    info                = models.ForeignKey('Info', on_delete=models.CASCADE, blank=True, null=True)
 

    def save(self,*args,**kwargs):     

        if self.pic and self.pic.file and self.pic.file.name != self.original_filename and isinstance(self.pic.file, TemporaryUploadedFile):
            self.original_filename = self.pic.file.name
            if self.pk:
                old_pic = self.__class__._default_manager.get(pk=self.pk)
                self.delete_discarded_images(old_pic)

        super().save(*args,**kwargs)


    # dzēš bildes un uzģenerētos thumbnailus pie, ja maina bildi tad dzēš vecās
    def delete_discarded_images(self, pic=None):
        paths = []
        pic_obj = pic if pic else self
        for f in dir(self.__class__):
            if isinstance(getattr(self.__class__, f), (ImageSpecField, ImageFileDescriptor)):
                sf = getattr(pic_obj,f,None)
                if sf:
                    paths.append(getattr(sf, 'path'))

        else:
            for i,path in enumerate(paths):
                p = Path(path)
                if p.is_file(): os.remove(path)

                try:
                    if not any(p.parents[0].iterdir()) and p.parents[0].is_dir():
                        shutil.rmtree(p.parents[0])

                    if not any(p.parents[1].iterdir()) and p.parents[1].is_dir():
                        shutil.rmtree(p.parents[1])

                except Exception as e:
                    pass

    def delete(self,*args,**kwargs):
        self.delete_discarded_images()
        super().delete(*args,**kwargs)

        