from django import forms
from django.contrib.auth.models import User



def add_attr(field,attr_name,attr_val):
    existing_attr = field.widget.attrs.get(attr_name,'')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_val}'.strip()



def add_placeholder(field,place_holder_val: str):
    field.widget.attrs['placeholder'] = place_holder_val.strip()


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
            help_text=(
                "Passwords must be equals"
            )
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
                'placeholder' : 'type your password here'
            })
        }