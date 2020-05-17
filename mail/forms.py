from django import forms


from .models import *
class fileForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True ,'blank': True, 'null': True }))

class messageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea)
    class Meta:
            model = Message
            fields = ['title','body', 'secrecy', 'number']


class signatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields  = ['text']



class group_messageForm(forms.ModelForm):
    class Meta:
            model = Group_message
            fields = ['users']

	





class Profile_form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'