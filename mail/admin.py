from django.contrib import admin

# Register your models here.
from .models import  (Message, 
File, 
Group_message, 
Folder, 
Profile,  
Signature, 
Shablon_message, 
Notificate, Company)

admin.site.register(Message)
admin.site.register(File)
admin.site.register(Group_message)
admin.site.register(Folder)
admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Signature)
admin.site.register(Shablon_message)
admin.site.register(Notificate)
