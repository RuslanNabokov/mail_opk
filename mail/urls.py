from django.urls import path
from .views import  Message, fileView, MessageDetail,  get_message, folderscreate, folderdelete, messagedel, searchmessage, ubrizkor
urlpatterns = [
    path('main/<str:sort_fold>', Message.as_view(),  name ='main'),
    path('message/<str:message_detail>', MessageDetail.as_view(), name = 'massage_detail'),
    path('createfolders/', folderscreate, name = 'createfolders'),
    path('ajaxpage/', get_message, name = 'ajax_get_message' ),
    path('new_message/', fileView.as_view(), name = 'new_masssage'),
    path('folderdelete/', folderdelete, name = 'folderdelete'),
    path('messagedel/', messagedel, name = 'messagedel'),
    path('ajax_calls/search/', searchmessage, name='searchmessage'),
    path('ubrizkor', ubrizkor, name='ubrizkor')



]
