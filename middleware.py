from django.contrib.auth import login as ln  # log out
from django.contrib.auth import logout  as lt
from mail.backends import *
from django.contrib.auth import login as ln  # log out
from django.contrib.auth import logout  as lt # 
from mail.backends import *
from django.utils.deprecation import MiddlewareMixin


class AuthLdapMiddleware(MiddlewareMixin):
    def process_request(self, request):
        self.request = request

        #user = request.META['REMOTE_USER'].split('@')[0]
       # user = ModelBackend.authenticate(request,username = login, password = 'musavi88')
       # if user is not None:
       #     if user.is_active:
       #         ln(request, user)
        
        return None

    
    
    def process_response(self,request, response):
        
        
        return response