from django import forms


from .models import *
class fileForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True ,'blank': True, 'null': True }))

class messageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea)
    class Meta:
            model = Message
            fields = ['title','body', 'secrecy']



class group_messageForm(forms.ModelForm):
    class Meta:
            model = Group_message
            fields = ['users']

	