from django.shortcuts import render

from main.models import Profile, AuthUser
from .models import * 
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponse,  HttpResponsePermanentRedirect

from django.views.generic.edit import FormView

from mail.models  import File

templates = {
   'massage_main': 'message_main.html',
}



SERVER = 'ftp://10.2.2.244'
'srv/gtp/upload'.replace('srv/', '').replace('ftp/', '')

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
