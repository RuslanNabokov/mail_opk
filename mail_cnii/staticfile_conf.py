import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')


STATIC_DIRS = 'static'


MEDIA_DIR = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
STATICFILES_DIRS =[
    STATIC_DIRS,
    os.path.join(BASE_DIR, 'static'),
    MEDIA_DIR,
    
]
#    'PASSWORD': '',
#    'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
#    'PORT': '5432',

