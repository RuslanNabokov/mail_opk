from  .models import Group_message, Message, Folder, Notificate
#from main.Model import Profile
from django.contrib.auth.models import User 
import pdb
from django.db.models import Q

from mail.models import Profile

def in_message_count(request):
    try:
        vhod = Group_message.objects.filter( Q(users__in=[request.user]) | Q(profile__in=[Profile.objects.get(user=request.user)  ]) ).exclude(message__in = [i  for  i in Folder.objects.get(specificate='trush', user = request.user).message.all()] ).count()
    except Exception:
        vhod = Group_message.objects.filter( users__in=[request.user] ).exclude(message__in = [i  for  i in Folder.objects.get(specificate='trush', user = request.user).message.all()] ).count()
    favorite = Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'favorite').message.all().count
    trush =  Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'trush').message.all().count
    favorite_id =  Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'favorite').pk
    trush_id =  Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'trush').pk
    return {'vhod_count': vhod, 'favorite_count': favorite, 'trush_count': trush.count(), 'favorite_id': favorite_id, 'trush_id': trush_id}

def auth_ldap(request):
     try:
        username, domain = request.META['REMOTE_USER'].split('@')   # return domain  user and domain namep
        request.user = User.objects.get(username = username)
        return {'auth':  request.user}
     except Exception:
        raise 'not user {}, domain {}'.format(username, domain)



def req_us(request):
    username, domain = request.META['REMOTE_USER'].split('@')
    user = User.objects.get(username = username)
    return {'req_us': user, 'domain':domain} 


def prof(request):

    username, domain = request.META['REMOTE_USER'].split('@')   # return domain  user and domain namep
    #username = request.user
    '''
    try:
        prof = Profile.objects.get(user=AuthUser.objects.get(username=username))
    except Exception:
        prof = username
    '''
    try:

        prof = Profile.objects.get(user=User.objects.get(username=username)) if username else  Profile.objects.get(user=request.user)
    except Exception as e:
        
        prof = 'none'
    
    #pdb.set_trace()
    return {'prof_c': prof}


def dost_prof(request):
    user = User.objects.get(username = request.user)
    dos =  Profile.objects.filter(Q(host__in = [user]))

    return {'prof_dos':dos}

def nmes(request):
    user = User.objects.get(username = request.user)
    prof_host = Profile.objects.filter(host__in= [user])
    mes_nansw  = Group_message.objects.filter( Q(users__in=[user]) | Q(profile__in = [i for i in prof_host] ) ).exclude(have_read__in=[user]).count()
    return {'nepr_soobsh': mes_nansw}


def notificate(request):
    notificate = [i for i in  Notificate.objects.filter(user = User.objects.get(username = request.user)) if i.active()]
    c  = {}
    if any(notificate):
        for i in notificate:
            i.view_user()
            c[i.pk] = [i.result, i.message]
            #pass 
    return {'notificate': notificate}