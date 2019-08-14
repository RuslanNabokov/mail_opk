from django.db import models
from main import * 
from django.db.models.signals import post_save, post_init, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from mail.models import Folder

# Create your models here.



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'







class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

  



@receiver(post_save, sender=User)
def post_save_us(sender, instance, **kwargs):
    print(instance)
    print(kwargs)
    Folder.objects.create(user=instance,name='trush', description='trush', specificate='trush').save()
    Folder.objects.create(user=instance,name='favorite', description='favorite', specificate='trush').save()



class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)







#################################################################
class Company(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    prefix_d = models.CharField(max_length=25)
    information = models.CharField(max_length=500)


    def __str__(self):
        return 'Компания {}'.format(self.name) 

 

class Employe(models.Model):
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)
    position = models.CharField(max_length=12)
    tolerance_level = models.IntegerField()
    company = models.ForeignKey(Company, models.DO_NOTHING)

    def __str__(self):
        return 'Работник {}'.format(self.first_name)




class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(db_column='Description', max_length=200)  # Field name made lowercase.
    company = models.ForeignKey(Company, models.DO_NOTHING)

    def __str__(self):
        return 'Profuct comany - {} || name {}'.format(company.name, self.name)

 


class Profile(models.Model):
    position = models.CharField(max_length=12)
    first_name_d = models.CharField(max_length=12)
    last_name_d = models.CharField(max_length=12, blank=True, null=True)
    tolerance_level = models.IntegerField()
    activate = models.BooleanField()
    role = models.CharField(max_length=12, blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, related_name='Юзер', on_delete=models.CASCADE)



    def __str__(self):
        return 'Profile {}|| login  {}'.format(self.first_name_d, self.user.username)  



