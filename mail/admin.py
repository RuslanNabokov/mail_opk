from django.contrib import admin

# Register your models here.
from .models import  * 

admin.site.register(Message)
admin.site.register(File)
admin.site.register(Group_message)
admin.site.register(Folder)
