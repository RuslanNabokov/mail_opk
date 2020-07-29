from django.contrib.auth.models import User
from mail_cnii import settings as st
import logging
logger = logging.getLogger(__name__)
"""
декоратор для постоянной аунтификации  пользователя 


"""


def ldap_auth(fun):
      def gh( *args, **kwargs):
         """
         Место для логера
         """
         
         try:
            args = args[0].user = User.objects.get(username  = request.META['REMOTE_USER'].split('@')[0])
         except Exception as e:
            if st.DEBUG:
                   pass
            else:
                   raise e
         return fun(*args, **kwargs)
      return gh
   #  user = ModelBackend.authenticate(request,username = request.user, password = 'musavi88')
     # request.user = User.objects.get(username=username)


'''

def  anonim_user_not_in(fun):
   def gh(*args, **kwargs):
      if args[0].user == ""


'''