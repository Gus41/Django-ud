from django.test import TestCase
from django.urls import reverse,resolve
from recipes import views


class RecipeViewsTest(TestCase):
    
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipe:home'))
        self.assertIs(view.func,views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipe:category', kwargs={'id' : 1}))
        self.assertIs(view.func,views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipe:detail',kwargs={'id' : 1}))
        self.assertIs(view.func,views.recipe)

    #---------- status code view
    def test_recipe_home_view_returns_200_OK(self):
        response = self.client.get(reverse('recipe:home'))
        self.assertEqual(response.status_code,200)

    # template tests
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipe:home'))
        self.assertTemplateUsed(response,'recipes/pages/home.html')
    
