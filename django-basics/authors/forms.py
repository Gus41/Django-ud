from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import re



def add_attr(field,attr_name,attr_val):
    field.widget.attrs[attr_name] = f'{attr_val}'.strip()



def add_placeholder(field,place_holder_val: str):
    add_attr(field,'placeholder',place_holder_val)




def strong_password(password: str):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError("Password is not strong",code='invalid')
    

class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'],'placeholder','Type your username here')
        add_placeholder(self.fields['email'],'Type your email here')
    
    
    
    password2 = forms.CharField(
            required=True,
            widget= forms.PasswordInput(attrs={
                'placeholder' : 'Repeat your password here'
            }),
            error_messages={
                'required' : 'Password must not be empty'
            },
        )
    password = forms.CharField(
        required=True,
        #validators=[strong_password]
    )

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
                'placeholder' : 'Type your password here'
            })
        }

    
        
    def clean(self):
        cleaned_data = super().clean()        
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError({
                'password2': ValidationError('Passwords must be equal',code='invalid')
            })
        