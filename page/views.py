from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import logout
from django.http import HttpResponse

from core.helpers import is_htmx

from .utils import requires_authorization, reprocess_headers
from .forms import LoginForm



def index(request):
    if request.user.is_anonymous:
        return do_login(request)
    else:
        return render(request, 'index.html', { }) 

@requires_authorization
def do_logout(request):
    logout(request)
    if is_htmx(request):   
        return reprocess_headers(HttpResponse('/'), {'hx_redirect': '/'})
    else:
        return redirect('/')


def do_login(request):
    logged_in = False

    if request.POST:
        login_form = LoginForm(request.POST, request=request)
        if login_form.is_valid():
            logged_in = True
    else:
        login_form = LoginForm()

    if is_htmx(request):
        headers = {}
        if logged_in:
            headers['hx_redirect'] = '/'            

        rendered = render_to_string("components/login_form.html", {
            'login_form': login_form
        })

        return reprocess_headers(HttpResponse(rendered), headers)

    if logged_in:
        return redirect('/')

    return render(request, 'login.html', { 
        'initial': True,
        'login_form': login_form
    }) 