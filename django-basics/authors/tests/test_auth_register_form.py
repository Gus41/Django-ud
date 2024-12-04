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
        ('username',(
            'Username must have letter, numbers or one of those _-', # Just - and _ other charactes will not be accepted
            'The length should be between 4 and 50 characters.'
        ))
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
            ('username','Username')
    ])
    def test_labels_are_correct(self,field: str, label_nedded: str):
        form = RegisterForm() 
        label  = form[field].field.label
        
        self.assertEqual(label,label_nedded)

#---------------------------------------------------

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
        ('first_name','Write your first name'),
        ('last_name','Write your last name'),
        ('password','Password must not be empty'),
        ('password2','Pleas repeat your password'),
        ('email','Email is required'),
        ('username','Username must not be empty'),

    ])
    def test_fields_can_not_be_empty(self, field: str, msg: str):
        self.form_data[field] = ''
        url = reverse('auth:create')
        response = self.client.post(url,data=self.form_data,follow=True)
        
        self.assertIn(msg,response.context['form'].errors.get(field))
        
    def test_username_field_min_length_should_be_4(self):
        msg = 'Username must have at least four characters'
        self.form_data['username'] = '123'
        url = reverse('auth:create')
        response = self.client.post(url,data=self.form_data,follow=True)
        
        self.assertIn(msg,response.context['form'].errors.get('username'))
        
    def test_username_field_max_length_should_be_50(self):
        msg = 'Username must have less than 50 characters'
        self.form_data['username'] = 'a' * 51

        url = reverse('auth:create')
        response = self.client.post(url,data=self.form_data,follow=True)
        
        self.assertIn(msg,response.context['form'].errors.get('username'))
        
    def test_password_field_have_lowers_uppers_case_letters_and_numbers(self):
        msg = 'Password is not strong'
        self.form_data['password'] = 'just_letters'

        url = reverse('auth:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        errors = response.context['form'].errors.get('password', [])
        self.assertIn(msg, errors)

        # Valid pass
        self.form_data['password'] = 'V4l1DP4assw0rd'

        url = reverse('auth:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        errors = response.context['form'].errors.get('password', [])
        self.assertNotIn(msg, errors)
        
    def test_passwrods_must_be_equal(self):
        msg = 'Passwords must be equal'
        self.form_data['password'] = 'V4l1DP4assw0rd'
        self.form_data['password2'] = '0therPassword'
        url = reverse('auth:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        errors = response.context['form'].errors.get('password2', [])
        self.assertIn(msg, errors)
        
        # Valid pass
        
        self.form_data['password'] = 'V4l1DP4assw0rd'
        self.form_data['password2'] = 'V4l1DP4assw0rd'
        url = reverse('auth:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        errors = response.context['form'].errors.get('password2', [])
        self.assertNotIn(msg, errors)
        
        
    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('auth:create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,404)
        
        


