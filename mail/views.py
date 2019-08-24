from django.shortcuts import render

from main.models import Profile, AuthUser
from .models import * 
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponse

from .models import  Group_message, File
from .models import   Message as massage
from .models import Folder
from  .forms import fileForm, messageForm,  group_messageForm
from django.views.generic.edit import FormView

from django.core.paginator  import Paginator 

from django.http import JsonResponse
from django_ajax.decorators import ajax

from django.views.decorators.http import require_GET 
from django.contrib.auth.decorators  import login_required
import json
from django.core import serializers

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.utils.timezone import make_aware

templates = {
   'massage_main': 'message_main.html',
   'message_new': 'mail_new_message.html',
   'massage_detail': 'massage_detail.html'
}



def req_user(obj, request):                                       # vozr user
      return  request.user



class MessageDetail(TemplateView):
    template_name = templates['massage_detail']
    def get(self, request, message_detail):
        self.message = massage.objects.get(pk=message_detail)
        self.users_message = Group_message.objects.get(message=self.message).users.all()
        self.group =  Group_message.objects.get(message=self.message)
        self.files = File.objects.filter(message= self.message)
        self.files.len  = len(self.files)
        if req_user(self, request) in self.users_message:
             return render(request, self.template_name, {'message': self.message, 'group': self.group, 'files': self.files, 'users_message': self.users_message})
        else:
            return HttpResponse('Доступ запрещен')

@csrf_protect
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


@csrf_protect
def messagedel(request):
    json_data = json.loads(request.body)
    id_messages  = json.loads(request.body)['messages']
    if id_messages:
        massage.objects.filter(pk__in=id_messages).delete()
    return JsonResponse({'status':'ok'})
    
@csrf_exempt
def folderdelete(request):
 
    json_data = json.loads(request.body)
    id_folders  = json.loads(request.body)['pk']

    if id_folders:
        Folder.objects.filter(pk__in=id_folders).delete()
    return JsonResponse({'status':'ok'})
    




@require_GET
def get_message(request, sort='all'):
     page = (request.GET['page'])
    # masname = [ 'message_title', 'owner', 'date' ]
     try:
         sort =  request.GET['sort']
     except Exception:
         sort = 'all'
     prof = req_user(None, request) 
     if sort == 'all':
        paginator = Paginator(Group_message.objects.filter(users__in=request.user), 10)
     else:
         pass
     c = {i.pk:[i.message.title, i.owner.user.username, i.lifetime] for i in paginator.page(page).object_list}
     return JsonResponse(c)



@require_GET
def searchmessage(request):
    q = request.GET.get('term', '')

    search_qs = AuthUser.objects.filter(username__startswith=q)
    results = []
    for r in search_qs:
        place_json = {}
        place_json['pk'] = r.id
     #   place_json['sec']=r.secrecy
        place_json['label'] = r.username 
        results.append(place_json)
    dat = json.dumps(results)
    HttpResponse(dat, 'application/json')

 #   c = {i.username: i.pk  for i in results  }
    return JsonResponse(results, safe=False) 


class Message(TemplateView):
     template_name = templates['massage_main']

     def get(self, request, sort_fold='all'):
        try:
            page = int(request.GET['page'])
        except Exception :
            page = 1
        self.prof = req_user(self, request)
        self.folders = Folder.objects.filter(user = AuthUser.objects.get(username = request.user))
        if sort_fold == 'all':
            self.message_user_auth =Paginator( Group_message.objects.filter(users__in=[request.user],  message__folder__specificate__in=['folder', None, 'faforite']   ), 10)
            print(self.message_user_auth.page(1).object_list)
        else:
            self.folder = Folder.objects.get(pk=sort_fold)
            self.message_user_auth  =  Paginator(Group_message.objects.filter(users__in=[request.user],message__in=[i  for i in self.folder.message.all() ]), 3)
        self.col_all_messages = self.message_user_auth.count

        return render(request, self.template_name, {'message': self.message_user_auth.page(page).object_list  ,'mes': self.message_user_auth.page(page), 'prof': request.user, 'folders': self.folders, 'col_all_messages': self.col_all_messages })





class fileView(FormView):
    form_class = fileForm
    template_name = templates['message_new']
    
   # template_name = 'upload.html'  # Replace with your template

    def post(self, request, *args, **kwargs):
        naive_datetime = datetime.datetime.now()
        self.prof = req_user(self, request)
        users = request.POST.get("names")  #####
        users   = AuthUser.objects.filter(username__in = users.split(','))
        print(users)
        form_class = self.get_form_class()
        form_file  = self.get_form(form_class)
        form_massage =  messageForm(request.POST)
        if  form_massage.is_valid():
               print('sdsd')
               obj_message = form_massage.save()
               obj_group =  Group_message.objects.create(owner = request.user, message = obj_message, lifetime = make_aware(naive_datetime))
               obj_group.users.set(users[::])
               print(obj_group.users)
               obj_group.save()
               message = obj_message
              # form_group.save()
               files = request.FILES.getlist('file_field')
               if form_file.is_valid():
                   for f in files:
                       v = File.objects.create(file = f, message = obj_message)
                   v.save() 
               return HttpResponse('сообщение отправлено')
        else:
            return  HttpResponse('ошибка')
            #self.form_invalid(form_file)
    def get(self, request):
           template_name = templates['message_new']
           form_file = fileForm()
           form_massage =  messageForm()
           form_group = group_messageForm()
           return render(request,  template_name, {'form_file': form_file, 'form_massage': form_massage, 'form_group': form_group})


# Create your views here.
