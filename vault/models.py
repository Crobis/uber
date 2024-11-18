from django.db import models
from django.utils.translation import get_language, gettext as _
from page.models import User

from libs.obfuscate_id import encode_id, decode_id


class Vault(models.Model):
    title               = models.CharField(_('Title'),max_length=250, blank=True)

    date_created        = models.DateTimeField(_('Izveidots'), auto_now_add=True, blank=True)
    date_modified       = models.DateTimeField(_('Labots'), auto_now=True, blank=True)
    user_created        = models.ForeignKey(User,verbose_name=_('Lietotājs izveidoja'),blank=True, null=True,related_name="user_created_vault", on_delete=models.CASCADE)
    user_modified       = models.ForeignKey(User,verbose_name=_('Lietotājs laboja'),blank=True, null=True,related_name="user_modified_vault", on_delete=models.CASCADE)


class Treasure(models.Model):
    vault               = models.ForeignKey(Vault, on_delete=models.CASCADE, null=True, blank=True)
    title               = models.CharField(_('Title'),max_length=250, blank=False)
    value               = models.TextField(_('Data'), blank=True)

    date_created        = models.DateTimeField(_('Izveidots'), auto_now_add=True, blank=True)
    date_modified       = models.DateTimeField(_('Labots'), auto_now=True, blank=True)
    user_created        = models.ForeignKey(User,verbose_name=_('Lietotājs izveidoja'),blank=True, null=True,related_name="user_created_treasure", on_delete=models.CASCADE)
    user_modified       = models.ForeignKey(User,verbose_name=_('Lietotājs laboja'),blank=True, null=True,related_name="user_modified_treasure", on_delete=models.CASCADE)

    def get_id(self):
        return encode_id(self.pk)


# class UserPin(models.Model):
#     user    = models.OneToOneField(User, on_delete=models.CASCADE)
#     pincode = models.DateField(null=True, blank=True)


