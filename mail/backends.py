
from django.contrib.auth.models import User
from django.contrib.auth import login as ln 

class ModelBackend(object):
    '''
    Extending to provide a proxy for user
    '''


    def authenticate(request, username=None, password=None):
        try:
            username, domain = request.META['REMOTE_USER'].split('@')
        except Exception:
            pass
        user =  User.objects.get(username=username)
        ln(request, user)
        return user
        
    
    def get_user(self, user_id):
        
        return User.objects.get(pk = user_id)
