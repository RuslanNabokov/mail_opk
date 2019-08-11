from django.urls import path
from .views import  Message, fileView, MessageDetail,  get_message, folderscreate, folderdelete

urlpatterns = [
    path('main/<str:sort_fold>', Message.as_view(),  name ='all_message'),
    path('message/<str:message_detail>', MessageDetail.as_view(), name = 'massage_detail'),
    path('createfolders/', folderscreate, name = 'createfolders'),
    path('ajaxpage/', get_message, name = 'ajax_get_message' ),
    path('new_message/', fileView.as_view(), name = 'new_masssage'),
    path('folderdelete/', folderdelete, name = 'folderdelete')


]
