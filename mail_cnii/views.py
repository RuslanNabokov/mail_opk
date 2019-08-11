from django.shortcuts import render
from django.http import HttpResponse
from .models import *

from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as ln  # log out
from django.contrib.auth import logout  as lt # in

def req_user(obj, request):                                       # vozr user
      return Profile.objects.get(user = request.user)


def login(request, login):
    user = authenticate(request,username = login, password = 'musavi88')
    if user is not None:
        if user.is_active:
            ln(request, user)
            return HttpResponse('Authenticate ok!')
        else:
            return HttpResponse('disable account')
    else:
        return HttpResponse('invalid login')



def logout(request):
    if request.user:
        lt(request)
        return HttpResponse('Logout')

    else:
        return HttpResponse('no')


