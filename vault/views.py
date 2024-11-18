import base64
import logging
import os
import traceback
import json
import datetime
import time

from functools import wraps
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from render_block import render_block_to_string

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.html import mark_safe as ms
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from core.helpers import is_ajax, is_htmx, random_string
from libs.obfuscate_id import encode_id, decode_id

from page.utils import build_top_menu, reprocess_headers, requires_authorization
from .forms import ModifyTreasure
from .models import Treasure, Vault

# secret = "Some secret"
# print(Fernet.generate_key())
# # Generate a salt for use in the PBKDF2 hash
# salt = base64.b64encode(os.urandom(12))  # Recommended method from cryptography.io
# # Set up the hashing algo
# kdf = PBKDF2HMAC(
#     algorithm=SHA256(),
#     length=32,
#     salt=str(salt),
#     iterations=100000,  # This stretches the hash against brute forcing
#     backend=default_backend(),  # Typically this is OpenSSL
# )
# # Derive a binary hash and encode it with base 64 encoding
# hashed_pwd = base64.b64encode(kdf.derive(user_pwd))

# # Set up AES in CBC mode using the hash as the key
# f = Fernet(hashed_pwd)
# encrypted_secret = f.encrypt(secret)


# encrypted_secret, algo, iterations, salt = db.get('some-user')

# # Set up the Key Derivation Formula (PBKDF2)
# kdf = PBKDF2HMAC(
#     algorithm=SHA256(),
#     length=32,
#     salt=str(salt),
#     iterations=int(iterations),
#     backend=default_backend(),
# )
# # Generate the key from the user's password
# Generate the key from the user's password
# key = base64.b64encode(kdf.derive(user_pwd))

# # Set up the AES encryption again, using the key
# f = Fernet(key)

# # Decrypt the secret!
# secret = f.decrypt(encrypted_secret)
# print("  Your secret is: %s" % secret)


def get_custom_key(pin):
    pin = str.encode(pin)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=settings.ENCRYPT_KEY.encode(),
        iterations=480000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(pin))

# 25579729
def encrypt(value, pin=''):
    try:
        value   = str(value)
        pin     = str(pin)
        key     = settings.ENCRYPT_KEY
        if pin:
            key = get_custom_key(pin)


        cipher_pass     = Fernet(key)
        encrypt_pass    = cipher_pass.encrypt(value.encode('ascii'))
        encrypt_pass    = base64.urlsafe_b64encode(encrypt_pass).decode("ascii")
        return encrypt_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(value, pin=''):
    try:
        key = settings.ENCRYPT_KEY
        if pin:
            key = get_custom_key(pin)

        value       = base64.urlsafe_b64decode(value)
        cipher_pass = Fernet(key)
        decod_pass  = cipher_pass.decrypt(value).decode("ascii")
        return decod_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None





def requires_pin(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):      
        if is_htmx(request):
            
            if 'vault_pin' not in request.session:
                # if 'pk' in kwargs:

                #     treasure = get_object_or_404(Treasure, pk=kwargs['pk'])

                # if function.__name__ == 'view_treasure':
                #     response = enter_pincode( request, request.GET.get('sub_action') )                    
                # elif function.__name__ == 'modify_treasure':
                #     response = enter_pincode(request, 'get_inline_form' )
                #     request.POST = {}     
                # elif function.__name__ == 'modify_treasure':


                response = enter_pincode(request, 'get_inline_form' )
                request.POST = {}    


                if isinstance(response, dict):                                           
                    request.new_headers = response
                else:
                    return response 
        else:
            return redirect('/')

        return function(request, *args, **kwargs)
    return wrap






@requires_pin
def modify_treasure(request, pk=None):
    # time.sleep(1)
    # for meta in request.META.items():
    #     if 'HX' in meta[0]:
    #         print(meta)

    headers     = {}
    treasure    = None
    initial     = {}
    action_url  = reverse('vault:add_treasure')
    sub_action  = request.POST.get('sub_action')
    form_id     = random_string(10)

    if pk:        
        treasure = get_object_or_404(Treasure, pk=pk)
        action_url = reverse('vault:edit_treasure', kwargs={'pk': treasure.id} )
        initial['decoded_value'] = decrypt(treasure.value)
    
    if request.POST:

        form = ModifyTreasure(request.POST, instance=treasure)
        if form.is_valid():
            # time.sleep(10)
            treasure = form.save()
            treasure.value = encrypt(form.cleaned_data['decoded_value'], request.session['vault_pin'])
            treasure.save()

            # if sub_action == 'save_inline_form':
            #     return view_treasure(request, treasure.id)
  
    else:
        form = ModifyTreasure(instance=treasure, initial=initial)    

    rendered = render_to_string("vault/components/edit_treasure.html", {
        'form': form,
        'action_url': action_url,
        'form_id': form_id,
        'treasure': treasure
    })
   
    return reprocess_headers(HttpResponse(rendered), getattr(request,'new_headers', {}))


    
def enter_pincode(request, sub_action):

    data = {
        'hx_retarget': '#main_modal',
        'hx_trigger': 'showModal',
        'hx_reswap': 'none',
    }   
    error = ''



    # if sub_action == 'reveal_inline':
    #     action_url = reverse('vault:view_treasure', kwargs={'pk': treasure.id})
    # elif treasure:
    #     action_url = reverse('vault:edit_treasure', kwargs={'pk': treasure.id})
    # else:
    #     action_url = reverse('vault:add_treasure')


    action_url = request.get_full_path()

    if request.POST:
        print(request.POST)
        pin = request.POST.get('pincode', None)
        if pin != None:
            value = '111' #decrypt(treasure.value, pin)
            if value == '111':
                data['hx_trigger']  = 'hideModal'
                # data['hx_retarget'] = f'#treasure_{treasure.get_id()}'
                # data['hx_reswap']   = 'outerHTML'

                if action_url == reverse('vault:add_treasure'):
                    data['hx_retarget'] = '.list-group'
                    data['hx_reswap']   = 'afterbegin'

                request.session['vault_pin'] = pin
                request.session['vault_pin_modified'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return data

            else:
                error = _('Incorrect pin')



        

    rendered = render_to_string("vault/components/bs_modal_pincode.html", {
        'action_url': action_url,
        # 'treasure'  : treasure,
        'sub_action': sub_action,
        'error'     : error
    })

    data['body'] = rendered
    return show_modal(data)



def test(user):
    # print(user)
    return True

@user_passes_test(test,'/login/')
@requires_pin
def view_treasure(request, pk):
    # time.sleep(1)

    headers         = {}
    treasure        = get_object_or_404(Treasure, pk=pk)
    sub_action      = request.GET.get('sub_action') or request.POST.get('sub_action')
    decoded_data    = None

    if sub_action == 'reveal_inline' and 'vault_pin' in request.session:
        decoded_data = decrypt(treasure.value, request.session['vault_pin'])

    rendered = render_to_string("vault/components/list_treasure.html", {
        'treasure': treasure,
        'decoded_data': decoded_data
    })

    return reprocess_headers(HttpResponse(rendered), getattr(request,'new_headers', {}))



@require_http_methods(['GET','DELETE'])
def delete_treasure(request, pk=None):
    if not pk:
        return HttpResponse('')

    treasure        = get_object_or_404(Treasure, pk=pk)
    data = {
        'hx_retarget': '#main_modal',
        'hx_trigger': 'showModal',
        'hx_reswap': 'none',
        'buttons': [],
    }   

    data['buttons'] = [
        ms(f'<button type="button" class="btn btn-danger" data-bs-dismiss="modal" hx-delete="{reverse('vault:delete_treasure', kwargs={'pk': treasure.id})}" hx-target="#treasure_{treasure.get_id()}" hx-swap="outerHTML swap:1s">Yes</button>'),
        ms('<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>'),
    ]
    
    data['body'] = f'Delete treasure: {treasure.title}?'
        

    if request.method == 'DELETE':
        return HttpResponse('')
    else:
        return show_modal(data)
        









def show_modal(data):

    defaults = {
        'show': {
            'header': False,
            'footer': False
        },
        'title': '',
        'body': 'modal body',     
        'buttons': [],
        'hx_retarget': '',
        'hx_trigger': '',
        'hx_reswap': '',

    }

    defaults.update(data)    

    rendered = render_to_string("components/bs_modal.html", {
        'data': defaults
    })

    defaults['hx_custom_rendered'] = rendered

    response = HttpResponse(rendered)    
    return reprocess_headers(response, defaults)  



# @user_passes_test(test,'/login/')
# @user_passes_test(lambda u:not u.is_anonymous,'/admin/login/')

@requires_authorization
@require_http_methods(["GET"])
def list_treasures(request):

    print('pincode',request.user.pincode)

    # request.user.pincode = 'asd'
    # request.user.save()

    if 'vault_pin' in request.session:
        del request.session['vault_pin']

    if 'vault_pin_modified' in request.session:
        del request.session['vault_pin_modified']


    data = Treasure.objects.filter(user_created=request.user)
    rs = random_string(20)

    if is_htmx(request):
        return HttpResponse(render_block_to_string('vault.html', 'main_content', { 
            'htxm_request': True,
            'random_string': rs,
            'data': data,
        }))
    else:

        return render(request, 'vault.html', {
            'data': data,
            'top_menu': build_top_menu('/'),
            'random_string': rs
        }) 


# http://192.168.88.120:8989 sonarr
# http://192.168.88.121:9696 prowler 0125