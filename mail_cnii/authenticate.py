from django.conf import settings
from django.contrib.auth.models import User, check_password

class SettingsBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:
"""
    ADMIN_LOGIN = 'hex'
    ADMIN_PASSWORD = 'pbkdf2_sha256$150000$vfoQAtJ2w67r$mTf5ULQaZrlDHzvZ17Q8jJygNWx5I7T/kcu5IuqIHsg='

    def authenticate(self, username=None, password=None):
        login_valid = (ADMIN_LOGIN == username)
        pwd_valid = check_password(password, ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = User(username=username, password='12345678')
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None