import ldap
from django_auth_ldap.config import LDAPSearch
import os
DEBUG = True

ALLOWED_HOSTS = ['*']


#KRB5_REALM = 'MIL.RU'
#KRB5_SERVICE = '[hostname]/MIL.RU'

# Enabled KDC verification defending against rogue KDC responses
# by validating the ticket against the local keytab.
#KRB5_VERIFY_KDC = True

# Enable case-sensitive matching between Kerberos and database user names
#KRB5_USERNAME_MATCH_IEXACT = True

# redirect url after login
#LOGIN_REDIRECT_URL = '/'


LDAP_SERVER = 'srv.mil.ru'
AUTH_LDAP_SERVER_URI = 'ldap://srv.mil.ru'
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_BIND_DN = 'uid=admin,cn=users,dc=mil,dc=ru'				#'cn=avicomp2,dc=mil,dc=ru'
AUTH_LDAP_BIND_PASSWORD =  'zxCV67RT' 	#os.environ.get('MY_PASS')  			#'123456'
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=users,dc=mil,dc=ru", ldap.SCOPE_SUBTREE, "(uid=%(user)s)"
)



# enable kerberos auth backends
AUTHENTICATION_BACKENDS = (
      #"django.contrib.auth.backends.ModelBackend",
    "django_auth_ldap.backend.LDAPBackend",
	 "django.contrib.auth.backends.ModelBackend",
#    'django_auth_kerberos.backends.KrbBackend',
)

AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=users,dc=MIL,dc=RU"
AUTH_LDAP_ALWAYS_UPDATE_USER = True


AUTH_LDAP_USER_ATTR_MAP = {
            "first_name": 'LOGNAME'
  	   # "last_name": "sn",
}

#AUTH_LDAP_USER_ATTR_MAP = {
#    "username": "sAMAccountName",
#    "first_name": "givenName",
#    "last_name": "sn",
#    "email": "mail",
#}


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
#        'NAME': 'mail_22',
#        'USER': 'postgres',
        #'PASSWORD': '',
        #'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        #'PORT': '5432',
#    }
#}
