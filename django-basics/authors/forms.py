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
        add_placeholder(self.fields['username'],'Type your username here')
        add_placeholder(self.fields['email'],'Type your email here')
        add_placeholder(self.fields['password'],'Type your password here')
        add_placeholder(self.fields['password2'],'Repeat your password here')
        add_placeholder(self.fields['first_name'],'Type your name here')
        add_placeholder(self.fields['last_name'], 'Type your last name here')
    
    
    password2 = forms.CharField(
        required=True,
        widget= forms.PasswordInput(),
        error_messages={
        'required' : 'Pleas repeat your password'
        },)
    
    password = forms.CharField(
        required=True,widget=forms.PasswordInput(),error_messages={
        'required' : 'Password must not be empty'
        },
        validators=[strong_password],
        label='Password'
    )
    
    first_name = forms.CharField(
        required=True,error_messages={
        'required':"Write your first name"
        },
        label="First name"
    )
    
    last_name = forms.CharField(
        required=True,error_messages={
        'required':"Write your last name"
        },
        label="Last name"
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': "Email is required"
        },
        label="E-mail",
        help_text = 'The e-mail must be valid'
    )
    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letter, numbers or one of those _-', # Just - and _ other charactes will not be accepted
            'The length should be between 4 and 50 characters.'
        ),
        min_length=4,
        max_length=50,
        required=True,
        error_messages={
            'required': 'Username must not be empty',
            'min_length' : 'Username must have at least four characters',
            'max_length': 'Username must have less than 50 characters'
        }
        
    )

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        exists = User.objects.filter(email=email)
       
        if len(exists) > 0:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )
        return email
        
    def clean(self):
        cleaned_data = super().clean()        
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError({
                'password2': ValidationError('Passwords must be equal',code='invalid')
            })
        