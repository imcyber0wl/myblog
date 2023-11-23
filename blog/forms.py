from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class WriteForm(forms.Form):
    title=forms.CharField(label="Title",required=True, max_length=250)
    img=forms.ImageField(required=False,)
    content=forms.CharField(label="Article",required=True,widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']
        
class EditProfileForm(forms.Form):
    img=forms.ImageField(required=False,)
    name=forms.CharField(label="Name",required=True, max_length=250)
    bio=forms.CharField(label="Bio",required=True,widget=forms.Textarea)

    
    
