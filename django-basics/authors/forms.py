from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']

        labels = {
            'username' : 'Username',
            'first_name' : "First name",
            'last_name' : 'Last name',
            'email' : 'E-mail',
            'password' : 'Password'
        }
        help_texts = {
            'email' : 'The e-mail must be valid.'
        }
        widgets = { 
            'first_name' : forms.TextInput(attrs={
                'placeholder' : 'username here',
                'class' : 'text-input other-class yadayada'
            }),
            'password' : forms.PasswordInput(attrs={
                'placeholder' : 'type your password here'
            })
        }