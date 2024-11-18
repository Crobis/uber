from django.urls import path, include

from .views import list_treasures, modify_treasure, view_treasure, enter_pincode, show_modal, delete_treasure



app_name = "vault"
urlpatterns = [
    path('modal/', show_modal),
    path('treasure/add/', modify_treasure, name='add_treasure'),
    path('treasure/delete/', delete_treasure, name='delete_treasure'), 

    path('<hashids:pk>/treasure/view/', view_treasure, name='view_treasure'),
    path('<hashids:pk>/treasure/delete/', delete_treasure, name='delete_treasure'), 
    # path('<hashids:pk>/treasure/reveal/', view_treasure, name='view_treasure'),
    # path('<hashids:pk>/treasure/view/', edit_treasure, name='view_treasure'),
    path('<hashids:pk>/treasure/edit/', modify_treasure, name='edit_treasure'),    
    # path('<hashids:pk>/treasure/delete/', edit_treasure, name='delete_treasure'),

    # path('<int:pk>/treasure/', edit_treasure),
    path('', list_treasures),
]
