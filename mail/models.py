from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_init, pre_save, post_delete

from django.dispatch import receiver
from django.db.models import signals
import os
import uuid
from datetime import datetime
from django.contrib.auth.models import User as AuthUser

# Create your models here.
ROLE = (
    ('admin',  'admin'),
     ('user',  'user'),
      ('redactor',  'redactor'),
      ('profile',  'profile')
)


LEVELS= (
    (0, 'Несекретно'),
    (3,'Для служебного пользования'),
    (2,'Секретно'),
    (1,'Совершенно Секретно')
)

SPETIFICATE =(
      ('folder', 'folder'),
      ('trush', 'trush' ),
      ('favorite', 'favorite'),
      ('send', 'send'),
      ('inbox','inbox')
)


RESULT_NOTIFICATE =(
      ('succes', 'succes'),
      ('error', 'error' ),
      ('warning', 'warning')
)




class Signature(models.Model):
    text = models.CharField(max_length=100)
    user = models.ForeignKey(AuthUser, related_name='signature', on_delete=models.CASCADE, blank=True, null=True)  

    def __str__(self):
        return 'signature  - {}'.format(self.user) 


class Company(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    prefix_d = models.CharField(max_length=25)
    information = models.CharField(max_length=500)
    img = models.ImageField(upload_to='upload', blank=True, null=True)


    def __str__(self):
        return 'Компания {}'.format(self.name)
    
    def img_path(self):
        
        mas = self.img.path.split('/')
        media_ind = mas.index('media')
        return  "/".join(mas[media_ind:])



class Profile(models.Model):
    position = models.CharField(max_length=12)
    first_name_d = models.CharField(max_length=12)
    last_name_d = models.CharField(max_length=12, blank=True, null=True)
    surname = models.CharField(max_length=20, blank=True, null=True)
    tolerance_level = models.IntegerField(choices=LEVELS, blank=True, null=True)
    activate = models.BooleanField( blank=True, default=True)
    role = models.CharField(max_length=12, blank=True, null=True, choices = ROLE)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True,null=True)
    user = models.ForeignKey(AuthUser, related_name='Юзер', on_delete=models.CASCADE, blank=True, null=True)
    host = models.ManyToManyField(AuthUser, related_name='Пользователи_которым_доступна_почта', blank=True, null=True)



    def __str__(self):
        try:
            return 'Profile {}|| login  {}'.format(self.first_name_d, self.user.username)  
        except Exception:
            return 'prof'
    
    def img_(self):
        try:
            company = Profile.objects.get(user=self.user).company
            img = company.img_path()
            return img
        except Exception as e:
     
            return 'undefiend'

    def nepr_message_user(self):
        group = Group_message.objects.filter(profile__in=[self]).exclude(have_read__in=[self.user])
        return group


    def nepr_message_user_count(self):
        group = Group_message.objects.filter(profile__in=[self]).exclude(have_read__in=[self.user])
        return group.count()

    def nepr_message_all_host_count(self):
        group = Group_message.objects.filter(profile__in=[self]).exclude(have_read__in=[i for i in self.host.all() ])
        return group.count()


    def full_name(self):
        return '{} {}'.format(self.first_name_d, self.last_name_d)






def default_datetime():
      return datetime.now()


from  .setting_change_file import *

def get_file_path(instance, filename):
    name = filename    
    group =  Group_message.objects.filter(message = instance.message)[0]
    #+   datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S"
 #   if  not  os.path.exists('/srv/ftp/upload/' + path):
 #         os.makedirs('/srv/ftp/upload/' + path)

    return os.path.join('/','/home/ruslan/projects/mail_opk/media', group.owner.username, instance.name() )
    

#   file ``
class File(models.Model):
      ps = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      description  = models.CharField(max_length=25,blank=True, null=True)
      file  = models.FileField(upload_to=get_file_path, blank=True, null=True)
      message  = models.ForeignKey('Message', related_name='Сообщение', on_delete=models.CASCADE, blank=True, null=True)

      def name(self):
            return str(self.file).split('/')[-1] 

      def __str__(self):
            return self.file.name
        



class Folder(models.Model):
      name  = models.CharField(max_length=50)
      description = models.CharField(max_length=150, blank=True, null=True)
      user =  models.ForeignKey(AuthUser, related_name='user_to_folder', on_delete=models.CASCADE)
      message = models.ManyToManyField('Message', null=True, blank=True)
      specificate = models.CharField(max_length=20,blank=True,verbose_name='spec',null=True,default='folder', choices = SPETIFICATE)
      
      def __str__(self):
            return 'папка {} пользователя {} '.format(self.name, self.user.username)

'''
      def add(self):
          if self.specificate == 'Trush':
              print('___________________________________________________________--')
'''



class Message(models.Model):
      #  owner =  models.OneToOneField(Profile,on_delete=models.CASCADE,  verbose_name=_u"Отправитель")
    title = models.CharField(("Title"), max_length=150)
    body  = models.CharField(max_length=4000, blank=True, null=True)
    secrecy = models.IntegerField(choices = LEVELS )
    number = models.CharField(max_length=20, blank=True, null=True)
    

    def __str__(self):
          return self.title

    def full_message(self):
        
        group = Group_message.objects.get(message=self)
        user = group.owner
        try:
            sign = Signature.objects.get(user=user) 
            return "{} </br> </br> {}".format(self.body, sign.text ) 
        except Exception:
            return "{}".format(self.body)

    def sinopsis(self):
        try:
            ret =   self.body[:190].replace('<br\>', '').replace('<br>', "") if len(self.body) < 190 else self.body[:190].replace('<br\>', '').replace('<br>', "") 
        except Exception: 
            ret =  ''
        return ret 
    
    def group(self):
        return Group_message.objects.get(message = self)





class Notificate(models.Model): # action or notificate
    user  = models.ForeignKey(AuthUser, verbose_name='пользователь', on_delete=models.DO_NOTHING)
    result = models.CharField(max_length=40,blank=False,choices=RESULT_NOTIFICATE) 
    allowed_to_view = models.BooleanField(default=True)                 # rasreshenno prosmotry
    message = models.CharField(max_length=25, blank=True, null=True)
    viewed_by_user = models.BooleanField(default=False)
    id_t  = models.CharField(null=False,max_length= 50, unique = True)  # prosmotrenno 

    def active(self):
        return bool(self.allowed_to_view and not self.viewed_by_user)
    def view_user(self):
        self.viewed_by_user  =  True
        self.save()
        return True 


class Group_message(models.Model):
    owner  = models.ForeignKey(AuthUser, on_delete=models.CASCADE, verbose_name=u"Пользователь", related_name = 'otprav', blank=True, null=True)
    users = models.ManyToManyField(AuthUser,  verbose_name = "Получатели почты", related_name = 'users', blank=True, null=True)
    profile = models.ManyToManyField(Profile, verbose_name='Получатель из профилей', related_name = 'profile', blank=True,null=True)
    message = models.ForeignKey(Message, verbose_name='Message', related_name = 'message', on_delete = models.CASCADE, blank=True, null=True )
    have_read = models.ManyToManyField(AuthUser, verbose_name= "Кто прочел", related_name = 'dsds', blank=True)
    lifetime = models.DateTimeField(default=default_datetime, null=True, blank=True)
    
    sending_message= models.ForeignKey('Group_message', related_name='send_essage', verbose_name='Ответ на',  on_delete=models.CASCADE, blank=True, null=True)
    answer_message =  models.ForeignKey('Group_message', verbose_name='ответ на  сообщение',on_delete = models.CASCADE, blank=True, null=True )
    received = models.ManyToManyField(AuthUser,related_name='poluchili',  verbose_name= "Кто получил", blank=True)


    def __str__(self):
          return 'группа сообщения '  if not self.sending_message else 'группа сообщения. владелец - {}. номер - {}   ответ на '.format(self.owner.username, self.message.number, self.sending_message)
    def files(self):
        files =  File.objects.filter(message=self.message)
        return files
    def save(self,message='Сообщение созданно', *args, **kwargs):
        try:
            try:
                Group_message.objects.get(pk = self.pk)
                Notificate.objects.create(user = self.owner, result='succes',message= message,id_t =  datetime.now().strftime("%d-%m-%Y %H:%M%S")).save()
            except Exception:
                
                Notificate.objects.create(user = self.owner, result='succes',message= 'Сообщение создано',id_t =  datetime.now().strftime("%d-%m-%Y %H:%M%S")).save()
        except Exception:
            pass 

        return super(Group_message, self).save()    

    

  

class Shablon_message(models.Model):
    owner  = models.ForeignKey(AuthUser, on_delete=models.CASCADE, verbose_name=u"Shablon", related_name = 'shablo', blank=True, null=True)
    name=  models.CharField(max_length=50, null=False, blank = False)
    text =   models.CharField(max_length=7000,  null=False, blank=False)

    class Meta:
        unique_together = (("owner", "name"),)
    def __str__(self):
        return 'shablon: {}, user: {} '.format(self.name, self.owner.username)


@receiver(post_save, sender=Group_message)
def post_save_Group(sender,instance, **kwargs):
    if  not instance.users.all():
        return 
    user = instance.owner
    users_wher_bilo_soobsh = Folder.objects.filter(message = instance.message)
    for fold in users_wher_bilo_soobsh:
        fold.message.remove(instance.message)
    folder_send = Folder.objects.get(user=instance.owner,specificate='send')
    folder_send.message.add(instance.message)
    fold_in_user =  Folder.objects.filter(user__in= instance.users.all(), specificate='inbox')

    #map(lambda x: x.message.add(instance.message),  fold_in_user)
   
    for i in instance.users.all():
        Notificate.objects.create(user = i, result='succes',message= 'У вас новое сообщение',id_t =   uuid.uuid1()).save()
        instance.have_read.remove(i)
    for i in fold_in_user:
        i.message.remove(instance.message)
        if not instance.message in i.message.all():
            i.message.add(instance.message)
        



@receiver(post_save, sender=File)
def post_save(sender,instance, **kwargs):
    message = instance.message
    group = message.group()
    for i in group.users.all():
        path = PATH_FILES_USERS + i.username
        os.system(f'cp {instance.file}  {path} ')
        print(f'cp {instance.file}  {path} ' )



@receiver(post_delete, sender=Message)
def post_delete(sender, instance, **kwargs):
    try:
        Group_message.objects.get(message = instance).remove()
    except Exception:
        pass








