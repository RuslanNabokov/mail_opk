from  .models import Group_message, Message, Folder, Notificate
#from main.Model import Profile
from django.contrib.auth.models import User 
import pdb
from django.db.models import Q

from mail.models import Profile

def decor_local_host_dev(func):
        def fu(arg):
            #arg.user= User.objects.all()[0]
            return func(arg)   #if arg.META['HTTP_HOST'] != '127.0.0.1:8000'  else {'':''} 
        return fu
"""
 ДОступ к сообщениям с любой страницы 

"""


@decor_local_host_dev
def in_message_count(request):
    try:
        vhod = Group_message.objects.filter( Q(users__in=[request.user]) | Q(profile__in=[Profile.objects.get(user=request.user)  ]) ).exclude(message__in = [i  for  i in Folder.objects.get(specificate='trush', user = request.user).message.all()] ).count()
    except Exception:
        vhod = Group_message.objects.filter( users__in=[request.user] ).exclude(message__in = [i  for  i in Folder.objects.get(specificate='trush', user = request.user).message.all()] ).count()
    favorite =  Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'favorite')
    trush =  Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'trush')
    send =  Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'send')
    inbox =  Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'inbox')
    return {'vhod_count': inbox.message.count(),   'favorite': favorite, 'trush': trush, 'send': send, 'inbox': inbox}
"""
Аунтификация


"""
'''
@decor_local_host_dev
def auth_ldap(request): 
    try:
        username, domain = request.META['REMOTE_USER'].split('@')   # return domain  user and domain namep
        request.user = User.objects.get(username = 'user')
        return {'auth':  request.user}
    except Exception:
        raise 'not user {}, domain {}'.format(username, domain)

'''

''' 
Возращает аунтифицированного 


'''


@decor_local_host_dev
def auth_ldap(request): 
    try:
        username, domain = request.META['REMOTE_USER'].split('@')   # return domain  user and domain namep
        request.user = User.objects.get(username = 'user')
        return {'auth':  request.user}
    except Exception:
        return {'auth':  request.user}
 
@decor_local_host_dev
def req_us(request):
    try:
        username, domain = request.META['REMOTE_USER'].split('@')   
    except Exception:
        username, domain  = request.user, 'localhost'
    return {'req_us': username, 'domain':domain} 
    

@decor_local_host_dev
def prof(request):
    username = request.user
    '''
    try:
        prof = Profile.objects.get(user=AuthUser.objects.get(username=username))
    except Exception:
        prof = username
    '''
    try:
        prof = Profile.objects.get(user=User.objects.get(username=username))
    except Exception as e:
        
        prof = 'none'
    #pdb.set_trace()
    return {'prof': prof}

'''
Возращает профили,  на которые есть права чтения сообщений данного пользователя

'''

@decor_local_host_dev
def dost_prof(request):
    user = User.objects.get(username = request.user)
    dos =  Profile.objects.filter(host__in = [user] )
    return {'prof_dos':dos}


@decor_local_host_dev
def nmes(request):
    user = User.objects.get(username = request.user)
    prof_host = Profile.objects.filter(host__in= [user])
    mes_nansw  = Group_message.objects.filter( Q(users__in=[user]) | Q(profile__in = [i for i in prof_host] ) ).exclude(have_read__in=[user]).count()
    return {'nepr_soobsh': mes_nansw}

'''
@decor_local_host_dev
def notificate(request):
    notificate = [i for i in  Notificate.objects.filter(user = User.objects.get(username = request.user)) if i.allowed_to_view and  not i.viewed_by_user]
    c  = {}
    if any(notificate):
        for i in notificate:
            i.view_user()
            c[i.pk] = [i.result,i.message]
            #pass 
    return {'notificate': notificate}
'''