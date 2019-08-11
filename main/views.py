from django.shortcuts import render
from django.http import HttpResponse
from .models import *

from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.mixins import PermissionRequiredMixin  #
# Create your views here.


def req_user(obj, request):                                       # vozr user
      us  = AuthUser.objects.get(username = request.user)
      return Profile.objects.get(user = us)


def organizations(request):
      org = Company.objects.all()
      return render(request, 'organizations.html', {'org': org}  )

def home(request):
    return render(request, 'main.html', {'prof': req_user(None, request)} )