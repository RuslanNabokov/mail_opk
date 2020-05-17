from django.shortcuts import render

from main.models import Profile, AuthUser
from .models import * 
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponse,  HttpResponsePermanentRedirect

from django.views.generic.edit import FormView

from mail.models  import File
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

templates = {
   'massage_main': 'message_main.html',
}

import os


'''
SERVER = 'ftp://10.2.2.244'
'srv/gtp/upload'.replace('srv/', '').replace('ftp/', '')
'''


def poligon(request):
   files = request.GET['names'].split(',')
   files = File.objects.filter(pk__in= files)
   files = ' '.join(list(map( lambda x: x.file.path, files  ) ))
    
   return render(request,  "vue_files.html",{'files':files} )

def get_content_dir(request):
   user = request.user
   root_path = '/home/{}'.format(user)
   dirs = []
   files = []
   answer = {} # otvet
   get_transition_path  = request.GET['get_transition_path']
   get_transition_dir =  root_path   +  get_transition_path + '/'
   print(get_transition_dir)
   for root, dirs_, files_ in os.walk(get_transition_dir):
      dirs.append(dirs_)
      files.append(files_)
      root = root
      break
   dirs = list(filter(lambda x: x[0] != '.' ,dirs[0]) )
   answer['dirs'] = dirs
   #answer['path']  =    root 
   return JsonResponse(answer,safe=False)
   
  # resutl = ["tmp",'home','Documents']
  # resp = JsonResponse(resutl, safe=False) 
  # return resp 
#    return JsonResponse({'name': "name"})

# функция перемеш

@csrf_exempt
def send_files(request):
   user = request.user

#   import pdb; pdb.set_trace()
   files = request.POST['files'].split(',')
   
   dir_  = request.POST['dir_'].replace(' ','\ ')

   for i in  files:
      os.system('cp {}   /home/{}{}'.format(i,user,dir_))

   



def req_user(obj, request):                                       # vozr user
      us  = AuthUser.objects.get(username = request.user)
      return Profile.objects.get(user = us)




class getFile(FormView):
   # template_name = templates['massage_new']

   # template_name = 'upload.html'  # Replace with your template
    def get(self, request, file):
           file = File.objects.get(ps=file)
           path = str(file.file).replace('srv/', '').replace('ftp', '')
           print(path)
           return  HttpResponsePermanentRedirect('{}{}'.format(SERVER,path))


# Create your views here.
