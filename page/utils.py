from django.template.loader import render_to_string

import json
from functools import wraps

from core.helpers import is_htmx
from page.forms import SearchForm




def build_top_menu(request, url=None):

    menu = [
        ['Home','/'],
        ['Tags','/tags/'],
        ['Vault','/vault/'],
        ['Logout','/logout/'],
    ]

    search_form = ''
    if request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            pass

    return render_to_string('components/top_menu.html', {
        'menu': menu,
        'user': request.user,
        'main_search_form': search_form
    })


def reprocess_headers(response, new):

    if 'hx_retarget' in new and new['hx_retarget']:
        response['HX-Retarget'] = new['hx_retarget']

    if 'hx_trigger' in new and new['hx_trigger']:        
        
        if new['hx_trigger'] == 'showModal':
            response['HX-Trigger'] = json.dumps({
                'showModal': new['hx_custom_rendered']
            })
        else:
            response['HX-Trigger'] = new['hx_trigger']

    if 'hx_reswap' in new and new['hx_reswap']:
        response['HX-Reswap'] = new['hx_reswap']

    if 'hx_redirect' in new and new['hx_redirect']:
        response['HX-Redirect'] = new['hx_redirect']

    return response


def requires_authorization(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):      

        if request.user.is_anonymous:

            if is_htmx(request):
                 return redirect('/login/')
                # @user_passes_test(lambda u:not u.is_anonymous,'/admin/login/')
                
                # if 'vault_pin' not in request.session:
                #     # if 'pk' in kwargs:

                #     #     treasure = get_object_or_404(Treasure, pk=kwargs['pk'])

                #     # if function.__name__ == 'view_treasure':
                #     #     response = enter_pincode( request, request.GET.get('sub_action') )                    
                #     # elif function.__name__ == 'modify_treasure':
                #     #     response = enter_pincode(request, 'get_inline_form' )
                #     #     request.POST = {}     
                #     # elif function.__name__ == 'modify_treasure':


                #     response = enter_pincode(request, 'get_inline_form' )
                #     request.POST = {}    


                #     if isinstance(response, dict):                                           
                #         request.new_headers = response
                #     else:
                #         return response 
            else:
                return redirect('/login/')

        return function(request, *args, **kwargs)
    return wrap

# qm set 117 -scsi1 /dev/disk/by-id/ata-WDC_WD20EFRX-68EUZN0_WD-WCC4MHKFS4LT 