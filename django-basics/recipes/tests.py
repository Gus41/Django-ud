from django.test import TestCase
from django.urls import reverse
#python manage.py test

class RecipeURLsTest(TestCase):
    
    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipe:home')
        self.assertEqual(home_url,'/')

    
