from projects.models import WorkHours
from datetime import datetime,date
from staticpage.models import *
from projects.models import Domain,Client
from invoice.models import Invoice
from page.models import UserProfile
from page.views import gen_menu

def midw(request):
    started_work = False
    today = date.today()
    try:
        workhour = WorkHours.objects.filter(user=request.user,started__day=today.day,started__month=today.month,started__year=today.year,finished__isnull=True)
    except:
        workhour = None


    userprofile = None
    if request.user and request.user.id:
        userprofile = UserProfile.objects.get_or_create(user=request.user)

    if workhour:
        started_work = True

    # if 'USER' in request.session and 'MAIL' in request.session:
    # print type(request.path)

    #pagarina sesiju par sesijas esošo garumu ja useris ir aktīvs
    request.session.set_expiry(request.session.get_expiry_age())



    is_worker = request.user.groups.filter(name__in=['Darbinieki'])
    debts = ''
    if not is_worker and request.user.is_authenticated() and request.user.groups.filter(id__in=[2,5]):
        debts =  Invoice.objects.filter(client__id__in=Client.objects.filter(users__in=[request.user]).values_list('id',flat=True).distinct(),status__id=29).count()

    # print request.session.get('SUBMENU','project')
    submenu =  request.session.get('SUBMENU','projects')
    if request.session.get('SUBMENU'):
        del request.session['SUBMENU']



    return {
        'is_worker'	: is_worker,
        'started_work'  : started_work,
        'public_menu'	: StaticPage.objects.filter(public=True,show_in_menu=True),
        'NTD'		: '', #NEW TEMPLATE DIR
        'email_admin': Domain.objects.filter(client__admins__id__in=[request.user.id],active=True),
        'user': request.user,
        'userprofile':userprofile,
        'client_debts': debts,
        'menu': gen_menu(request, submenu, request.session.get('CURRENT_MENU',['/','/']))
    }