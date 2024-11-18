from django.urls import path, include

from .views import list_notes, modify_note, list_tags, delete_note, view_note



app_name = "notes"
urlpatterns = [


    path('add/', modify_note, name='add_note'),
    path('edit/<int:note_id>/', modify_note, name='edit_note'),
    path('view/<int:note_id>/', view_note, name='view_note'),
    path('delete/<int:note_id>/', delete_note, name='delete_note'),
    

    path('tags/', list_tags, name='list_tags'),
    path('tag/<int:tag_id>/', list_notes, name='view_tag'),    

    path('<slug:note_id>', view_note, name='view_slug_note'), 

    path('', list_notes, name='list_notes'),
   

]
