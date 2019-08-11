from django.urls import path
from .views import home, organizations

urlpatterns = [
    path('', home, name ='home'),
    path('organizations/',  organizations, name ='organizations' )
    
]

