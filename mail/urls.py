from django.urls import path
from .views import  Message, fileView, MessageDetail,  get_message, folderscreate, folderdelete, messagedel, searchmessage, ubrizkor, infold, get_all_message,searc_mes, del_iz_fold, read_mes,answ_mes, createsignature ,get_shablons, get_users, notificates, currect_message, img_organization
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path('main/<str:sort_fold>', Message.as_view(),  name ='main'),
    path('message/<str:message_detail>', MessageDetail.as_view(), name = 'massage_detail'),
    path('createfolders/', folderscreate, name = 'createfolders'),
    path('ajaxpage/', get_all_message, name = 'ajax_get_all_message' ),
    path('ajaxpage_get/', get_message, name = 'ajax_get_message' ),
    path('new_message/', fileView.as_view(), name = 'new_masssage'),
    path('new_message/<int:pk>', fileView.as_view(), name = 'update_masssage'),
    path('folderdelete/', folderdelete, name = 'folderdelete'),
    path('messagedel/', messagedel, name = 'messagedel'),
    path('ajax_calls/search/', searchmessage, name='searchmessage'),
    path('ubrizkor', ubrizkor, name='ubrizkor'),
    path('in_fold',  infold, name='in_fold'),
    path('search_mes',    searc_mes, name='searc_mes'),
    path('del_iz_fold',    del_iz_fold, name='del_iz_fold'),
    path('read_mes', read_mes, name = 'read_mes'),
    path('answ_mes', answ_mes, name = "answ_mes"),
    path('createsignature', createsignature, name = "createsignature" ),
    path('get_shablons', get_shablons, name = "get_shablons"),
    path('get_users', get_users, name = "get_users") ,
    path('get_notificats', notificates, name="get_notificates"),
    path('currect_message', currect_message, name='currect_message'),
    path('img_organization', img_organization, name='img_organization'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
