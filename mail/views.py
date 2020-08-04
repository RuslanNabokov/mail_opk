from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from main.models import Profile, AuthUser
from .models import * 
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponse

from .models import  Group_message, File
from .models import   Message as massage
from .models import Folder
from .models import Signature, Shablon_message
from  .forms import fileForm, messageForm,  group_messageForm
from django.views.generic.edit import FormView
from mail.backends import *
from django.core.paginator  import Paginator 

from django.http import JsonResponse
#from django_ajax.decorators import ajax

from django.views.decorators.http import require_GET 
from django.contrib.auth.decorators  import login_required
import json
from django.core import serializers

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.utils.timezone import make_aware
from django.db.models import Q
from django.shortcuts import get_object_or_404 
from itertools import chain
from django.views.decorators.cache import cache_page
from django.template.context_processors import csrf
from   ldap_auth  import ldap_auth
import logging
logger = logging.getLogger(__name__)

templates = {
   'massage_main': 'message_main.html',
   'message_new': 'mail_new_message.html',
   'massage_detail': 'massage_detail.html'
}

#######################################





###############################################3
#def ldap_auth(request):
   #  user = ModelBackend.authenticate(request,username = request.user, password = 'musavi88')
#      username, domain = request.META['REMOTE_USER'].split('@')
#      request.user = User.objects.get(username=username)


def req_user(obj, request):                                       # vozr user
      return  request.user
''' 


создание подписей 

'''
page_on_list = 15


@csrf_exempt
@ldap_auth
def createsignature(request):
    
    user = User.objects.get(username = request.user)
    type  =  request.POST['type']
    text = request.POST['text']
    if str(type) == '2':  # type signatyre
        sig = Signature.objects.create(user= user, text = text)
        
        sig.save()
        if sig.id:

            Signature.objects.filter(user=user).exclude(pk=sig.id).delete()
            return JsonResponse({'status': "Старая подпись удалена. Создана новая подпись"})
        else:
            return JsonResponse({'error':'error'})
    elif str(type) == '1':    # type shablon
        try:
            name = request.POST['name']
            shablon = Shablon_message.objects.create(owner=user, text = text, name=name)
            shablon.save()
            if shablon.id:
                return JsonResponse({'status':'Шаблон был создан'}) 
        except Exception as error:
            return JsonResponse({'error': str(error)})


@csrf_protect
@ldap_auth
def img_organization(request):
    try:
 
        user = User.objects.get(username = request.GET['user'])
        company = Profile.objects.get(user= user).company
        img = company.img_path()
  
        return JsonResponse({'img': img  })
    except Exception as e:
        logger.warning("[ERROR]  "  + e)  
        return JsonResponse({'error':str(e)})



@csrf_protect
@ldap_auth
def answ_mes(request):
 
    message = Group_message.objects.filter(message = massage.objects.get(pk = request.GET['message'])).values( 'answer_message__message__pk', 'answer_message__pk',)
    #answ = message.answer_message.message.pkme

    answ,group_pk = message[0].values()
    #answ = message['answer_message']

    return JsonResponse({'answ':answ, 'group': group_pk}, safe=False)


@ldap_auth
def get_users(request):

    message = Group_message.objects.get(message = massage.objects.get(pk = request.GET['message']))
    ret = {}
    ret['users']  =  [ i.username for  i in message.users.all()]
    
    ret['profiles'] = [i.full_name() for i in message.profile.all()]
    return JsonResponse(ret, safe=False)
   # return JsonResponse({'users': [ "Авдурахман Иван Иванович", "Авдурахман Иван Иванович" ]}, safe=False)




@csrf_protect
@ldap_auth
def get_shablons(request):

    pk = request.GET['pk_mes']
    user =  User.objects.get(username = request.user)
    shablon  =  Shablon_message.objects.get( pk =  int(pk))
    dat = {}
    dat['name'] = shablon.name
    dat['text'] = shablon.text
    dat['pk'] = shablon.pk
    return JsonResponse(dat, safe=False)

@csrf_protect
@ldap_auth
def read_mes(request):
 
    message_id = request.GET['message']
    message = massage.objects.get(pk=message_id)
    users_message = Group_message.objects.get(message=message).users.all()
    group =  Group_message.objects.get(message=message)
    mes_dic = {}
    mes_dic['message'] =  [message.title, message.full_message()] 
    mes_dic['message_group'] = [group.owner.username, group.lifetime ]
    try:
        files = File.objects.filter(message= message)
        mes_dic['files']  =  [[i.ps, i.name() ]  for i in files ]
    except Exception:
        mes_dic['files'] = ""
    group.have_read.set([User.objects.get(username=request.user)])
    return JsonResponse(mes_dic, safe=False)
    
@ldap_auth
def in_ms(request, sort='-lifetime'):

    user =  User.objects.get(username = request.user)
    try:
        mes_us = Group_message.objects.filter(Q(users__in=[request.user]) | Q(profile__in=[Profile.objects.get(user=user)   ])  ).exclude(message__in = [i  for  i in Folder.objects.get(specificate='trush', user = request.user).message.all()] ).order_by(sort)
    except Exception:
        mes_us = Group_message.objects.filter(users__in=[request.user]  ).exclude(message__in = [i  for  i in Folder.objects.get(specificate='trush', user = request.user).message.all()] ).order_by(sort)
    return mes_us
@ldap_auth
def send_ms(request, sort='-lifetime'):
    return  Group_message.objects.filter(owner=request.user ).order_by(sort)



@ldap_auth
def fold_ms(request,pk_fold,sort ='-lifetime',prof_id=-1, filter='all'):
   
    user = User.objects.get(username =request.user)
    if prof_id:
       
        prof = Profile.objects.get(pk =prof_id)
        
        group = Group_message.objects.filter(Q(profile__in=[prof])).filter(message__in = [i  for  i in Folder.objects.get(user = request.user, pk= pk_fold).message.all()] ).order_by(sort)
     
    try:

        group = Group_message.objects.filter(Q(users__in=[request.user]) | Q(profile=Profile.objects.get(user=request.user) )   | Q(owner=request.user) | Q(profile__in=[Profile.objects.get(user=user)])   ).filter(message__in = [i  for  i in Folder.objects.get(user = request.user, pk= pk_fold).message.all()] ).order_by(sort)
    except Exception:
        group =  Group_message.objects.filter(Q(users__in=[request.user]) | Q(profile=Profile.objects.get(user=request.user))   | Q(owner=request.user)   ).filter(message__in = [i  for  i in Folder.objects.get(user = request.user, pk= pk_fold).message.all()] ).order_by(sort)
    if filter == 'with_files':
        group = group.filter(message__in=[i.message for i in File.objects.all()])
    if filter == 'no_read':
        group = group.exclude(have_read__in=[request.user])
    
    fold_trush_us =  Folder.objects.get(user=request.user, specificate='trush')
    act_fold = Folder.objects.get(pk = pk_fold)
    if not act_fold.specificate  == 'trush':
        group = group.exclude(message__in=  [i for i in   fold_trush_us.message.all() ] )
        
    return group.distinct() #  КОООСТЫЫЫЫЫЛЬЬ 

@ldap_auth
def prof_in_us(request,prof, sort = '-lifetime', filter='all'):
    user = User.objects.get(username = request.user)
    prof = Profile.objects.get(pk =prof)
    group = Group_message.objects.filter(profile__in=[prof]).order_by(sort)
    if filter == 'with_files':
        group = group.filter(message__in=[i.message for i in File.objects.all()])
    if filter == 'no_read':
        group = group.exclude(have_read__in=[request.user])
    return group.distinct() #  КОООСТЫЫЫЫЫЛЬЬ 



class MessageDetail(TemplateView):

    template_name = templates['massage_detail']
    @ldap_auth
    def get(self, request, message_detail):
        """

        Поиск сообщений  на которые данное сообщение является ответом


        """ 
        self.message = massage.objects.get(pk=message_detail)
        self.users_message = Group_message.objects.get(message=self.message).users.all()
        self.group =  Group_message.objects.get(message=self.message)
        self.sending_message = []
        try:
            group = self.group
            while group:
                if group.answer_message: 
                    self.sending_message.append(group.answer_message)
                group = group.answer_message
                print(group)

        except Exception as e:
          logger.warning("[ERROR]  "  + e)    

        
        self.profile_message =  self.group.profile.all()
        self.files = File.objects.filter(message= self.message)
        self.files.len  = len(self.files)

        self.user = User.objects.get(username = request.user)
        self.trush = Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'trush')
        self.favorite = Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'favorite')
        try: 
            self.infavorite =   Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'favorite', message__in=[self.message])
        except Exception:
            self.infavorite = None 
        if req_user(self, request) in self.users_message[::] or  (req_user(self, request) in   [self.group.owner]  ) or ( Profile.objects.filter(Q(user__in=[self.user]) |  Q(host__in = [self.user])  ) ):
             self.group.have_read.set([User.objects.get(username=request.user)])
             return render(request, self.template_name, {'sending_message':self.sending_message ,'infavorite': self.infavorite, 'message': self.message, 'group': self.group, 'files': self.files, 'users_message': self.users_message, 'trush':self.trush, 'favorite':self.favorite})
        else:
            return HttpResponse('Доступ запрещен')

@csrf_exempt
@ldap_auth
def folderscreate(request,names='sd'):

    res = {}
    names = request.POST['name']
    description = request.POST['description'] or 'папка'
    if  len(Folder.objects.filter(name= names ).filter(user = AuthUser.objects.get(username = request.user))):
            res['error'] = 'папка с таким именем существует'
            return JsonResponse(res, safe=False)
    else:
        res = Folder.objects.create(name= names, description = description, user = AuthUser.objects.get(username = request.user))
        res.save()
        res = Folder.objects.filter(name= names, user = AuthUser.objects.get(username = request.user))[0]
        res = {'name': res.name, 'description':  res.description, 'id':  res.pk} 
    return JsonResponse(res, safe=False)
############# Функции  для работы с папками
@csrf_exempt
@ldap_auth
def infold(request):

    pk_mes = request.POST['pk_mes'].split(',')
    pk_fold = request.POST['pk_fold'] #json_data['pk_fold']
    mess = massage.objects.filter(pk__in=[int(i) for i in pk_mes])
    try:
        pk_in_er =  Folder.objects.get(user = AuthUser.objects.get(username = request.user),pk=pk_fold, message__in=mess)
        pk_not_in = mess.exclude(pk__in = [i for i in pk_in_er.message.all() ]) 
    except Exception:
         pk_in_er = []
    res =   Folder.objects.get(user = AuthUser.objects.get(username = request.user),pk=pk_fold)
    if (mess and res) and  (not pk_in_er or pk_not_in):
        res.message.add(*mess)
        return JsonResponse({'status':pk_mes})
    elif pk_in_er:
        return JsonResponse({'status':'bd'})
    else:
         return JsonResponse({'status':pk_mes})

@csrf_exempt
@ldap_auth
def del_iz_fold(request):

#    json_data = json.loads(request.body)
#    mes =  json_data['pk_mes']
#    fold = json_data['pk_fold']
    mes = request.POST['pk_mes']
    fold =  request.POST['pk_fold']
    folder = Folder.objects.get(user=  AuthUser.objects.get(username=request.user),pk=fold )
    message = massage.objects.get(pk=mes)
    folder.message.remove(message)
    return JsonResponse({'status':'ok'})

"""
Удаление сообщений ! !  !!  ! !!  !


"""
@csrf_exempt
@ldap_auth
def messagedel(request):


    id_messages  = request.POST['pk'].split(',')
    id_messages = map(lambda x: int(x), id_messages)
    id_pk = request.POST['folder']
    iz_trush  = bool( Folder.objects.get(pk=id_pk).specificate == 'trush'  )

    messages = [i.message  for i in  Group_message.objects.filter(pk__in=id_messages).all()]
    if messages:
       try:
           if  not iz_trush: # Удаление сообщения  Надо доделать
               Folder.objects.get(user = User.objects.get(username = request.user),specificate='trush').message.add(*messages)
               for mes in messages:
                   if  all([i.specificate=="trush"  for i in  Folder.objects.filter(message=mes) ]):
                       mes.remove()

#               for i in Folder.objects.filter(user = User.objects.get(username = request.user)).exclude(specificate='trush'):
#                   i.message.remove(*messages)
           else:
                Folder.objects.get(user = User.objects.get(username = request.user),specificate='trush').message.remove(*messages)
               
       except Exception as e:
           logger.warning("[ERROR]  "  + e)    
           raise e

       # map(lambda x: x ,Group_message.objects.filter(owner=User.objects.get(username=request.user), message=massage.objects.filter(pk__in=id_messages)))
       return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'no'})
    

@csrf_exempt
@ldap_auth
def folderdelete(request):
    try: 
        id_folders = request.POST['pk[]']
    except Exception:
        id_folders = request.POST['pk']
#    json_data = json.loads(request.body)
#    id_folders  = json.loads(request.body)['pk']
    if id_folders:
        Folder.objects.filter(pk__in=[id_folders]).delete()
        return JsonResponse({'status':id_folders})
    else:
        return JsonResponse({'error':'error'})


@csrf_exempt
@ldap_auth
def ubrizkor(request):
    pass
'''
    id_messages  = request.POST['pk'].split(',')
    id_messages = map(lambda x: int(x), id_messages)
    messages = [i.message  for i in  Group_message.objects.filter(pk__in=id_messages).all()]
    if id_messages:
        Folder.objects.get(user = AuthUser.objects.get(username = request.user),specificate='trush').message.remove(*messages)
    return JsonResponse({'status':'ok'})
'''

############# Функции  для работы с папками



@require_GET
@ldap_auth
def get_message(request, sort='all'):
     page = (request.GET['page'])
    # masname = [ 'message_title', 'owner', 'date' ]
     try:
         sort =  request.GET['sort']
     except Exception:
         sort = 'all'
     prof = req_user(None, request) 
     if sort == 'all':
        paginator = Paginator(Group_message.objects.filter(users__in=request.user), page_on_list)
     else:
         pass
     c = {i.pk:[i.message.title, i.owner.user.username, i.lifetime, i.message.pk,  bool(i.answer_message)] for i in paginator.page(page).object_list}
     return JsonResponse(c)

def fav_or_404(request,mes):
    try:
        Folder.objects.get(user = User.objects.get(username = request.user),specificate='favorite', message__in = [mes] )
        return True 
    except Exception:
        return False

@csrf_exempt
@ldap_auth
def get_all_message(request, sort='all'):
    
     page =  int(request.POST['page']) 
     type =   request.POST['type']  if request.POST['type'] != 'all' else  Folder.objects.get(user=request.user, specificate='inbox').pk
     filter_m = request.POST['filter']
    # masname = [ 'message_title', 'owner', 'date' ] .order_by(self.sorted)
     try:
         sort =  request.POST['sort']
     except Exception:
         sort = '-lifetime'
     try:
         prof_id  =  request.POST['prof']    
         
     except Exception:
         prof_id = None
     prof_id  = prof_id  if  prof_id != 'undefiend' else None
     if not prof_id:

            paginator =  Paginator(fold_ms(request,type,sort,prof_id,filter_m), page_on_list)
     else:
         paginator = Paginator( prof_in_us(request,prof_id,sort, filter_m) , page_on_list ) 
         #paginator = Paginator( fold_ms(request,type,sort, prof_id), page_on_list ) 
     c =  {}
     for en , i in enumerate(paginator.page(page).object_list):
        
        try:
            prof = Profile.objects.get(user = i.owner)
            name_p =   prof.first_name_d + " " + prof.last_name_d + " "  + prof.surname + " " +   prof.company.name
        except Exception as er:
            name_p = i.owner.username
        c[en] = [i.pk,i.message.title, name_p, i.lifetime,i.message.pk, bool(i.answer_message), fav_or_404(request,i.message), strip_tags(i.message.sinopsis()),bool(request.user in i.have_read.all() or not request.user in i.users.all()),  str(request.user) ==  str(i.owner.username)   ]

        try:
            c[en].append(Profile.objects.get( user=i.owner ).img_())
        except Exception:
            pass

     if (len(paginator.page(page).object_list) < 1 ):
         c = {'status': 'empty'}
     else:
         c['paginator'] = [paginator.page(page ).number,paginator.page(page).paginator.num_pages, paginator.page(page).has_previous(),paginator.page(page).has_next()  ]
   #c['answ'] = {i.pk: i.answer_message.pk for i in   paginator.page(page).object_list  if bool(i.answer_message) }
     # num str   vsego str    imeetsya li predidush   im li sled
     try:
         c['notification'] = []
         for i in  Notificate.objects.filter(user = request.user):
             if   i.active():
                  c['notification'].append(i.message)
                  i.view_user()
     except Exception as e:
       logger.warning("[ERROR]  "  + e)    
       raise e
    

     try:
         c["count_messages"] =  []
         
         all_message = Group_message.objects.filter(users__in=[request.user])
         no_read_all_mes=   all_message.exclude(have_read__in=[request.user])
         trush_mes =   Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'inbox').message.all()
         favorite =  Folder.objects.get(user = User.objects.get(username = request.user), specificate = 'favorite').message.all()
         for i in [all_message.count(),no_read_all_mes.count(),trush_mes.count(), favorite.count()]:
             c["count_messages"].append(i)
     except Exception as e:
       logger.warning("[ERROR]  "  + e)    
       raise e

     return JsonResponse(c)





@csrf_exempt
@ldap_auth
def searc_mes(request):   #  poisk sredstvami  poiska po stanice 
    key =  request.POST['key']
    types = request.POST['type']
    search =   request.POST['search']
    filter =  request.POST['filter']
    user = User.objects.get(username = request.user)
    
    logger.info('[INFO] Выполнен поиск по сообщениям  | По name/author  {} |  Тип/Папка {} |  Слово  {} | Фильтр {}  | Пользователь {} '\
        .format(search, types, key, filter, user  ))
    #nepr = request.POST['nepr']
    page = 1
    try:
        prof_id = request.POST['prof']
        prof = Profile.objects.filter(pk = prof_id )
    except Exception as e:
            prof_id = None
    if prof_id :
        prof_id = request.POST['prof']
        prof = Profile.objects.filter(pk = prof_id )
        groups  = Group_message.objects.filter(profile__in=prof)
    else:
        groups =  Group_message.objects.filter(Q(users__in=[user])| Q(owner=user) )
    if types not in ['all']:
        groups =  groups.filter(message__in =Folder.objects.get( pk=types).message.all())
    elif types == 'all':
        groups =  groups
    if search == 'owner':
        
        groups = groups.filter(Q(owner__in=User.objects.filter(username__startswith= key)) | Q(owner__in=  [i.user for i in  Profile.objects.filter( Q(first_name_d__startswith= key) | Q(surname__startswith= key)      ) ]  )  )  
    else:
        message =  massage.objects.filter(title__startswith=key)
        groups = groups.filter(message__in = message)
 #   if nepr == 'true':
 #       groups =  groups.exclude(have_read__in=[request.user])
    if filter == 'with_files':
        groups = groups.filter(message__in=[i.message for i in File.objects.all()])
    if filter == 'no_read':
        groups = groups.exclude(have_read__in=[request.user])
    paginator =  Paginator(groups, 20)
    c = {}
    for en , i in enumerate(paginator.page(1).object_list):
        try:
            prof = Profile.objects.get(user = i.owner)
            name_p =   prof.first_name_d + " " + prof.last_name_d + " "  + prof.surname + " " +   prof.company.name
        except Exception as er:
            name_p = i.owner.username
        #c[en] = [i.pk,i.message.title, name_p, i.lifetime,i.message.pk, bool(i.answer_message), fav_or_404(request,i.message), i.message.sinopsis(),bool(request.user in i.have_read.all() or not request.user in i.users.all()),  str(request.user) ==  str(i.owner.username)   ]
        c[en] = [i.pk,i.message.title, name_p, i.lifetime,i.message.pk, bool(i.answer_message), fav_or_404(request,i.message), i.message.sinopsis(),bool(request.user in i.have_read.all() or not request.user in i.users.all()),  str(request.user) ==  str(i.owner.username)   ]
        try:
            c[en].append(Profile.objects.get( user=i.owner ).img_())
        except Exception:
            pass  
      #  c = {en:[i.pk,i.message.title, i.owner.username, i.lifetime,i.message.pk,  bool(i.answer_message), fav_or_404(request,i.message), i.message.sinopsis(), bool(request.user in i.have_read.all() or not request.user in i.users.all()  )  ]) }
    c['paginator'] = [paginator.page(page).number,paginator.page(page).paginator.num_pages, False,False  ]
    #c['paginator'] = [paginator.page(page).number,paginator.page(page).paginator.num_pages, paginator.page(page).has_previous(),paginator.page(page).has_next()  ]
    return JsonResponse(c, safe=False) 



"""
    try:
        prof_id  =  request.POST['prof']
        prof =  Profile.objects.get(pk = prof_id)
        
    except Exception:
        prof_id = None

    if search == 'owner':
        if type == 'all':
            group_us = Group_message.objects.filter(users__in=[request.user])
            pg = group_us.filter(owner__in=User.objects.filter(username__startswith=key))   # Поиск по сообщениям  ключ - Отправитель

            paginator = Paginator(pg, page_on_list) 
            #paginator = Paginator(Group_message.objects.filter(users__in=[request.user]), page_on_list)
            if prof_id:
                paginator = Paginator(Group_message.objects.filter(profile__in=[prof]), page_on_list)
        elif not prof_id:
            paginator = Paginator(Group_message.objects.filter(users__in=[request.user]).filter(message__in = [i  for  i in Folder.objects.get(user= request.user, pk=type).message.all()]), page_on_list)
        else:
            paginator = Paginator(Group_message.objects.filter(profile__in=[prof]).filter(message__in = [i  for  i in Folder.objects.get(user= request.user, pk=type).message.all()]), page_on_list)
    else:
        message =  massage.objects.filter(title__startswith=key)
        if type == 'all':
            if prof_id:
                paginator = Paginator(Group_message.objects.filter(profile__in=[prof],message__in=message ), page_on_list)
                print('no00')
            else:
                paginator = Paginator(Group_message.objects.filter(users__in=[request.user],message__in=message ), page_on_list)
                print('s')
            print(f'type: {type}, id_prof: {prof_id}')
    
        elif type == 'send':
            paginator = Paginator(Group_message.objects.filter(owner__in=[request.user],message__in=message ), page_on_list)
        else:
            import pdb; pdb.set_trace()
            paginator = Paginator(Group_message.objects.filter(users__in=[request.user], message__in=message).filter(message__in = [i  for  i in Folder.objects.get( pk=type).message.all()]), page_on_list)
    c = {en:[i.pk,i.message.title, i.owner.username, i.lifetime,i.message.pk,  bool(i.answer_message), fav_or_404(request,i.message), i.message.sinopsis(), bool(request.user in i.have_read.all() or not request.user in i.users.all()  )  ] for en , i in enumerate(paginator.page(1).object_list) }
    return JsonResponse(c, safe=False) 
"""





@ldap_auth
def notificates(request):
    notificate = [i for i in  Notificate.objects.filter(user = User.objects.get(username = request.user)) if i.allowed_to_view and  not i.viewed_by_user]
    c  = {}
    if any(notificate):
        for i in notificate:
            i.view_user()
            c[i.pk] = [i.result,i.message]
            #pass 
    print('1' * 50)
    dat = c
    return JsonResponse(dat, safe=False) 


@require_GET
@ldap_auth
def searchmessage(request):   # Поиск  пользователей
    ldap_auth(request)
    q = request.GET.get('term', '')
    search_qs = AuthUser.objects.filter(username__startswith=q)
    results = []
    if len(search_qs) > 0 :
        for r in search_qs:
            place_json = {}
            place_json['pk'] = r.id
        #   place_json['sec']=r.secrecy
            place_json['label'] = r.username 
            results.append(place_json)
    else:
        search_qs = Profile.objects.filter(Q(first_name_d__startswith=q) | Q(last_name_d__startswith=q) )
        for r in search_qs:
            place_json = {}
            try:
                place_json['pk'] =  r.user.pk
                place_json['pk_prof'] =  r.pk
            except Exception:
                    place_json['pk_prof'] =  r.pk
        #   place_json['sec']=r.secrecy
            place_json['label'] = "{} {} {} ({})".format(r.first_name_d,  r.last_name_d, r.surname, r.company.name)
            results.append(place_json)
    dat = json.dumps(results)


 #   c = {i.username: i.pk  for i in results  }
    return JsonResponse(results, safe=False) 



"""
Главная страница сообщений


""" 

class Message(TemplateView):
     template_name = templates['massage_main']

      
     @ldap_auth
     
     def get(self, request, sort_fold='all'):

        try:
            page = int(request.GET['page'])
        except Exception :
            page = 1
        self.prof = req_user(self, request)
        try:
             self.folders = Folder.objects.filter(user = User.objects.get(username = request.user) ).filter(specificate__in=['folder'])

        except:
            pass
        return render(request, self.template_name, {'folders':self.folders})













class fileView(FormView):
   
    form_class = fileForm
    template_name = templates['message_new']
   # template_name = 'upload.html'  # Replace with your template
    @ldap_auth
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        self.prof = request.user
        
        self.shablons =   Shablon_message.objects.filter(owner = AuthUser.objects.get(username = request.user))
        naive_datetime = datetime.datetime.now()
        users_n = request.POST.get("names")  #####
        users   = [ i  for i in   AuthUser.objects.filter(username__in = users_n.split(',')) ]
        logger.info('[INFO] Пользователь {}  Отправил письмо  {}'.format(request.user,''.join(users_n)  ))

        profiles_sear = list(filter(lambda x: len(x.split(' ')) > 1, users_n.split(',') ))
        prof_mass = []
    
        for i in profiles_sear:
            try:
                v = Profile.objects.get(first_name_d= i.split(' ')[0], last_name_d = i.split(' ')[1])
                if not v.user:
                    prof_mass.append(v)
                else:
                    users.append(v.user)


            except Exception as e :
                raise e
        
        form_class = self.get_form_class()
        form_file  = self.get_form(form_class)
        try:
            a = Group_message.objects.get(pk =request.POST.get('message_pk')).message
            form_massage =  messageForm(request.POST, instance= a )
        except Exception as e:
            form_massage =  messageForm(request.POST)

        # try:
        #     # menyaem sushetvuushee soobshenie
        #     a = massage.objects.get(pk =request.POST.get('message_pk'))
        #     form_massage =  messageForm(request.POST, instance= a )
        #     if  form_massage.is_valid():
        #         form_massage.update()
            
        # except Exception as e:
        #      # ыsozdaem soobshenie 
        #     form_massage =  messageForm(request.POST)
        #     if  form_massage.is_valid():
        #         group.message =  form_massage.save()
        #     print('$' * 20)
        #     print(e)
        #     raise e
        try:
            answer = request.POST.get("answer")
            answer = Group_message.objects.get(pk=answer)
            
        except Exception:
            answer = False
        try:

            pk = request.POST.get('message_pk')
            group = Group_message.objects.get(pk = pk)
            files =  request.FILES.getlist('file_field')
            if  (  not files and    group.message.body  ==  form_massage.data['body'] and    group.message.title  ==  form_massage.data['title']  and    [ i for i in users ] == [i for i in  group.users.all()]):                           #если сообщение не изменилось
                return redirect('main',sort_fold='all')


            if  form_massage.is_valid():
    
                group.message = form_massage.save()
            else:
                print(form_massage.errors )
  
            if answer:
                group.answer_message = answer
            if prof_mass:
                group.profile.set(prof_mass[::])
            if users:
                group.users.set(users[::])
            files = request.FILES.getlist('file_field')
        

            group.message.save()
            group.save(message="Сообщение обновленно")
            try:  
                for f in files:
                    v = File.objects.create(file = f, message = group.message)
                    v.save()
            except Exception:
                pass
            

        
            return redirect('main',sort_fold='all')


        except Exception as e:
            print(20 * 'I')
            print(e)
            self.shablons =   Shablon_message.objects.filter(owner = AuthUser.objects.get(username = request.user))
            if  (form_massage.is_valid() or form_massage.errors == "body"  ) :
                obj_message = form_massage.save()
                if answer:
                    obj_group =  Group_message.objects.create(owner = request.user, message = obj_message, lifetime = make_aware(naive_datetime), answer_message= answer)
                    obj_group.users.add(AuthUser.objects.get(pk =answer.owner.pk))
                else: 
                        obj_group =  Group_message.objects.create(owner = request.user, message = obj_message, lifetime = make_aware(naive_datetime))


                if users:
                    obj_group.users.set(users[::]) ################################
                if prof_mass:
                   
                    obj_group.profile.set(prof_mass[::])
                obj_group.save(message="Сообщение создано")
                message = obj_message
                # form_group.save()
                files = request.FILES.getlist('file_field')
                for f in files:
                    v = File.objects.create(file = f, message = obj_message)
                try:    
                        v.save()
                except Exception:
                        pass
                return redirect('main',sort_fold='all')
            else:

                return  HttpResponse(form_massage.errors)
            #self.form_invalid(form_file)
    @csrf_exempt
    @ldap_auth
    def get(self, request,pk='s'):
           

           self.shablons =   Shablon_message.objects.filter(owner = AuthUser.objects.get(username = request.user))
           template_name = templates['message_new']
           form_file = fileForm()
           try:
                instance_group =  get_object_or_404(Group_message, pk=pk)
                pk_mes = instance_group.message.pk
                instance_message = get_object_or_404(massage, pk=pk_mes)
                form_massage =  messageForm(instance=instance_message)
                form_group = group_messageForm(instance=instance_group)
                users = instance_group.users.all()
                try:
                    profiles = instance_group.profile.all()
                except Exception:
                    profiles = ''
                try:
                    instance_file = File.objects.filter(message=massage.objects.get(pk=pk_mes))
                    file_name =  ' '.join([str(i.file) for  i in instance_file])
                    
                except Exception as er:
                   file_name = ''
           except Exception as er:
                 users = ''
                 profiles = ''
                 form_file = fileForm()
                 form_massage =  messageForm()
                 form_group = group_messageForm()

           try:
               answer = request.GET['answer']  # groups
               answer = Group_message.objects.get(pk=answer)
               try:
                   users_answer = [ request.GET['user'] ]
                   users= User.objects.filter(pk__in=users_answer)
               
               except Exception as e:
                   print(e)

           except Exception as e:
               answer = ''

           return render(request,  template_name, {'form_file': form_file, 'form_massage': form_massage, 'form_group': form_group, 'answer': answer, 'pk': pk, 'shablons': self.shablons, 'csrf':csrf, 'users': users, 'profiles': profiles  })


@require_GET
@csrf_exempt
@ldap_auth
def currect_message(request):
     number = request.GET['number']
     result = {}
     try:
         get_object_or_404(massage,number=number)
         result['error']= 'Уже есть'
     except Exception:
         result['succes'] = ''
     return JsonResponse(result, safe=False) 
# Create your views here.
