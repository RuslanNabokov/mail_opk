from django.urls import path
from .views import  getFile, get_content_dir,poligon, send_files, search_dir

urlpatterns = [
  #  path('<str:file>', getFile.as_view(),  name ='file'),
     path('get_content_dir/', get_content_dir,  name ='get_content_dir'),
     path('poligon/', poligon,  name ='poligon'),
     path('search_dir/',  search_dir, name= "search_dir"),
     path('send_files', send_files, name='send_files')
     

]

