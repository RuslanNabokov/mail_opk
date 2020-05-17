from django.contrib.auth.models import User
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
         except Exception:
            pass

         return fun(*args, **kwargs)
      return gh
   #  user = ModelBackend.authenticate(request,username = request.user, password = 'musavi88')
     # request.user = User.objects.get(username=username)


'''

def  anonim_user_not_in(fun):
   def gh(*args, **kwargs):
      if args[0].user == ""


'''