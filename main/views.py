from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from mail.models import Company
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
import json
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import get_object_or_404 
from  main.models import Profile
from django.shortcuts import redirect

from .forms import CompanyForm

from django.contrib.auth.mixins import PermissionRequiredMixin  #

from ldap_auth import ldap_auth

# Create your views here.
@ldap_auth
def req_user(obj, request):                                       # vozr user
      try:
            us  = User.objects.get(username = request.user)
      except Exception:
            us = AuthUser.objects.get(username = request.user)
      try:
       Profile.objects.get(user = us)
       return Profile.objects.get(user=us)
      except Exception:
            return  us
@ldap_auth
def organizations(request):
      org = Company.objects.all()
      return render(request, 'organizations.html', {'org': org}  )
@ldap_auth
def home(request):
   # request.user  = User.objects.get(username = 'test')

    return render(request, 'main.html')
'''
def home(request):
   
     #username = settings.AUTH_LDAP_BIND_DN
     #password = settings.AUTH_LDAP_BIND_PASSWORD
     #auth = LDAPBackend()
     #User = auth.authenticate(request,username=username,password=password)
     #uid = request.user
     #user = LDAPBackend() 
     #return HttpResponse(user.authenticate_ldap_user)
     #return HttpResponse('ee')
     #return render(request, 'main.html', {'prof': } )
     username, domain = request.META['REMOTE_USER'].split('@')   # return domain  user and domain name
     try:
           prof = Profile.objects.get(user=AuthUser.objects.get(username=username))
     except Exception:
           prof = username
           

     return  render(request, 'main.html', {'prof': prof} )

'''



@ldap_auth
def create_users(request, pk=None):

      if request.method == "POST":
            try:
                  pk_updatemessage = request.POST.get('pk')
            except Exception:
                  return HttpResponse('s')
            
            first_name_d = request.POST.get('first_name_d')
            last_name_d = request.POST.get('last_name_d')
            position  = request.POST.get('position')
            try:
                  user  = User.objects.get(pk= request.POST.get('names'))
            except Exception:
                  user =  User.objects.get(username= request.user)
            user_own = AuthUser.objects.get(username=request.user)
            try:
                  company = Profile.objects.get(user=user_own).company
            except Exception:
                  company = Company.objects.all()[0]
            if pk_updatemessage:
                   pr = Profile.objects.filter(pk=pk).update(last_name_d=last_name_d, first_name_d=first_name_d, position=position,company = company, user= user ) 

            else:
                  pr = Profile.objects.create(last_name_d=last_name_d, first_name_d=first_name_d, position=position,company = company, user=user  )
            return HttpResponse('ok')
            
      else:
            if request.method == "GET":
                  try:
                        user_update =  Profile.objects.get(pk=pk)
                  except Exception:
                        user_update = None
                  return render(request, 'newp.html', {'user':user_update}) 
      




@ldap_auth
def my_profiles(request):

      try:
            user = User.objects.get( username = request.user)
            profile =  Profile.objects.get(user = user)
            if profile.role == 'redactor':
                  profiles = Profile.objects.filter(company = profile.company)
                  return render(request, 'my_profile.html', {'profile': profiles} )
            return HttpResponse('Forbiden')
      except Exception:
            return HttpResponse('У вас нет доступных профелей')

@ldap_auth
def  profile_user(request,user):

      user =   Profile.objects.get(pk=user)
      return render(request, 'profile_detail', {'user': user})
@ldap_auth
def  users_and_organizations(request):

      profile = Profile.objects.all()
      return render(request, 'profile.html', {'profile': profile} )



@ldap_auth
def searchusernewprof(request):

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
            place_json['pk'] =  r.user.pk
        #   place_json['sec']=r.secrecy
            place_json['label'] = r.first_name_d  + ' ' +  r.last_name_d
            results.append(place_json)
    dat = json.dumps(results)
    HttpResponse(dat, 'application/json')

 #   c = {i.username: i.pk  for i in results  }
    return JsonResponse(results, safe=False) 



@ldap_auth
def organization_detail(request, pk):
      organization =  Company.objects.get(pk=pk)
      return render(request, 'organization_detail.html', {'company': organization} )





@ldap_auth
def redactorganization(request, pk):
      organization =  get_object_or_404(Company, pk=pk)
      if request.method == "POST":
            form  = CompanyForm(request.POST, instance=organization)
            if form.is_valid():
                   organization = form.save(commit=False)
                   organization.save()
                   return redirect('organization', pk = organization.pk )
      else:
            form = CompanyForm(instance=organization)
      return render(request, 'setting_organization.html', {'form': form})
