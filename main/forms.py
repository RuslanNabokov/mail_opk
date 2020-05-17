from django import forms
from django.utils.translation import ugettext_lazy as _




from mail.models import Company


class CompanyForm(forms.ModelForm):
    information = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Company
        fields= ['name','information','location', 'img']

'''
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    prefix_d = models.CharField(max_length=25)
    information = models.CharField(max_length=500)
    img = models.ImageField(upload_to='upload', blank=True, null=True)

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

'''