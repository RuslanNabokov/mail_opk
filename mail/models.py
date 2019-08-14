from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_init, pre_save
from django.dispatch import receiver
from django.db.models import signals
import os
from  main.models import *
import uuid
from datetime import datetime
from django.contrib.auth.models import User as AuthUser
# Create your models here.

LEVELS= (
    (1,'1'),
    (2,'2'),
     (3,'3')
)

SPETIFICATE =(
      ('folder', 'folder'),
      ('trush', 'trush' ),
      ('favorite', 'favorite')
)

def default_datetime():
      return datetime.now()

class Message(models.Model):
  #  owner =  models.OneToOneField(Profile,on_delete=models.CASCADE,  verbose_name=_u"Отправитель")
    title = models.CharField(("Title"), max_length=50)
    body  = models.CharField(max_length=1000, blank=True, null=True)
    secrecy = models.IntegerField(choices = LEVELS )
    

    def __str__(self):
          return self.title



def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    path =  Group_message.objects.get(message = instance.message).owner.user.username  + '/' +  datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S") + '/'
    if  not  os.path.exists('/srv/ftp/upload/' + path):
          os.makedirs('/srv/ftp/upload/' + path)
    return os.path.join('/', 'srv','ftp','upload', path,filename)

#   file 
class File(models.Model):
      ps = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      description  = models.CharField(max_length=25,blank=True, null=True)
      file  = models.FileField(upload_to=get_file_path, blank=True, null=True)
      message  = models.ForeignKey(Message, related_name='Сообщение', on_delete=models.CASCADE, blank=True, null=True)

      def name(self):
            return str(self.file).split('/')[-1] 

      def __str__(self):
            return self.file.name



class Folder(models.Model):
      name  = models.CharField(max_length=50)
      description = models.CharField(max_length=150, blank=True, null=True)
      user =  models.ForeignKey(AuthUser, related_name='user_to_folder', on_delete=models.CASCADE)
      message = models.ManyToManyField(Message, null=True, blank=True)
      specificate = models.CharField(max_length=20,blank=True, null=True,default='folder', choices = SPETIFICATE)
      

      def __str__(self):
            return 'папка {} пользователя {} '.format(self.name, self.user.username)

      





class Group_message(models.Model):
    owner  = models.ForeignKey(AuthUser, on_delete=models.CASCADE, verbose_name=u"Пользователь", related_name = 'otprav', blank=True, null=True)
    users = models.ManyToManyField(AuthUser,  verbose_name = "Получатели почты", related_name = 'users')
    message = models.ForeignKey(Message, verbose_name='Message', related_name = 'message', on_delete = models.CASCADE, blank=True, null=True )
    have_read = models.ManyToManyField(AuthUser, verbose_name= "Кто прочел", related_name = 'dsds', blank=True)
    lifetime = models.DateTimeField(default=default_datetime, null=True, blank=True)
    
    def __str__(self):
          return 'группа сообщения. владелец - {}'.format(self.owner.username)
  