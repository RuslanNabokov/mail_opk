import os
import sys	
sys.path.append('/home/hexedit/projects/mail/mail_opk/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mail_cnii.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
