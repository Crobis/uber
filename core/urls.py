"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, register_converter
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from libs.obfuscate_id import HashidsConverter

from page.views import  do_login, do_logout, index

register_converter(HashidsConverter, 'hashids')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('vault/', include('vault.urls', namespace='vault')),
    
    path('login/', do_login, name='login'),
    path('logout/', do_logout, name='logout'),
    # path('', index, name='index'),
    path('', include('notes.urls', namespace='notes')),  

    # path('', include('notes.urls')),
    # path('', TemplateView.as_view(template_name='base.html')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)