from django.urls import path
from .views import  getFile

urlpatterns = [
    path('<str:file>', getFile.as_view(),  name ='all_message')

]

