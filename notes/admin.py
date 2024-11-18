from django.contrib import admin

from .models import Picture, Note
# Register your models here.


@admin.register(Picture)
class PictureAdminForm(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user_modified = request.user
        if not obj.pk:
            obj.user_created = request.user

        super().save_model(request, obj, form, change)

@admin.register(Note)
class NoteAdminForm(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user_modified = request.user
        if not obj.pk:
            obj.user_created = request.user

        super().save_model(request, obj, form, change)