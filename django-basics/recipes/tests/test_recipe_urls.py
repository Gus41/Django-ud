from django.test import TestCase
from django.urls import reverse
#python manage.py test

class RecipeURLsTest(TestCase):
    
    def test_recipe_home_url_is_correct(self):
        url = reverse('recipe:home')
        self.assertEqual(url,'/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipe:category', kwargs={'id' : 1})
        self.assertEqual(url,'/recipes/category/1')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipe:detail',kwargs={'pk' : 1})
        self.assertEqual(url,'/recipes/1/')

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipe:search')
        self.assertEqual(url,'/recipes/search/')