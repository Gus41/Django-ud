from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized



class AuthRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username','Type your username here'),
        ('password','Type your password here'),
        ('password2','Repeat your password here'),
        ('email','Type your email here'),
        ('first_name','Type your name here'),
        ('last_name','Type your last name here'),
    ])

    def test_placeholders_are_correct(self,field : str, placeholder_expected: str):
        form = RegisterForm() 
        placeholder = form[field].field.widget.attrs['placeholder']
        
        self.assertEqual(placeholder_expected,placeholder)