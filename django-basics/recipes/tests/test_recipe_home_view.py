from django.urls import reverse,resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeHomeViewsTest(RecipeTestBase):
    

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipe:home'))
        self.assertIs(view.func.view_class,views.RecipeListViewHome)


    def test_recipe_home_view_returns_200_OK(self):
        response = self.client.get(reverse('recipe:home'))
        self.assertEqual(response.status_code,200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipe:home'))
        self.assertTemplateUsed(response,'recipes/pages/home.html')


    def test_recipe_homes_template_show_no_recipes_founded_if_no_recipes(self):

        response = self.client.get(reverse('recipe:home'))
        self.assertIn('No recipes found...',response.content.decode('utf-8'))

        
    def test_recipe_home_temaplte_loads_recipes(self):
        nedded_title = 'Recipe created'
        self.make_recipe(title=nedded_title)
        response = self.client.get(reverse('recipe:home'))
        response_content = response.content.decode('utf-8')
        self.assertIn(nedded_title,response_content)
        #self.fail('Falhar teste por n motivos')

    def test_recipe_home_temaplte_dont_load_recipes_not_published(self):
        nedded_title = 'This recipe will not apear'
        self.make_recipe(title=nedded_title,is_published=False)
        response = self.client.get(reverse('recipe:home'))
        response_content = response.content.decode('utf-8')
       
        self.assertNotIn(nedded_title,response_content)

   
            
        

