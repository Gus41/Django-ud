from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized

#this test are using TestCase from unittest, not from django

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


    @parameterized.expand([
        ('email','The e-mail must be valid'),
    ])
    def test_helptexts_are_correct(self,field : str, help_text_nedded: str):
        form = RegisterForm() 
        help_text  = form[field].field.help_text
        
        self.assertEqual(help_text,help_text_nedded)

    @parameterized.expand([
            ('username', 'Username'),
            ('first_name', "First name"),
            ('last_name', 'Last name'),
            ('email', 'E-mail'),
            ('password', 'Password'),
    ])
    def test_labels_are_correct(self,field: str, label_nedded: str):
        form = RegisterForm() 
        label  = form[field].field.label
        
        self.assertEqual(label,label_nedded)


from django.test import TestCase as DJTestCase
from django.urls import reverse

class AuthoRegisterIntegrationTest(DJTestCase):
    def setUp(self, *args, **kwargs):
        #valid data 
        self.form_data = {
            'username' : 'userTest',
            'first_name': 'name',
            'last_name': 'last',
            'email': 'test@email.com',
            'password': 'str0ngp4assw0rd',
            'password2': 'str0ngp4assw0rd'
        }

        return super().setUp(*args, **kwargs)
    

    @parameterized.expand([
        ('password', 'Password must not be empty'),
    ])
    def test_fields_can_not_be_empty(self, field: str, msg: str):
        self.form_data[field] = ''
        url = reverse('auth:create')
        response = self.client.post(url,data=self.form_data,follow=True)
        self.assertIn(msg,response.content.decode("utf-8"))

