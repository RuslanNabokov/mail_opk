from django.urls import path
from .views import home, organizations,users_and_organizations, create_users,searchusernewprof, my_profiles, organization_detail,redactorganization
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path('', home, name ='home'),
    path('organizations/',  organizations, name ='organizations' ),
    path('profiles/', users_and_organizations,  name='profiles'),
    path('createusers/', create_users,  name='create_users'),
    path('createusers/<int:pk>', create_users,  name='create_users'),
    path('myprofiles/', my_profiles, name = "myprofiles" ),
  
    path('searchusernewprof', searchusernewprof, name= 'searchusernewprof'),
    path('organization/<int:pk>', organization_detail, name='organization'),
    path('redactorganization/<int:pk>', redactorganization, name='redactorganization' )
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

