from django.urls import reverse,resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeHomeViewsTest(RecipeTestBase):
    

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipe:home'))
        self.assertIs(view.func,views.home)


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

    #@patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_is_paginated(self):
        
        for i in range(9):
            kwargs = {
                'author_data': {'username' : f'u{i}'},
                'slug' : f'r{i}'
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipe:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages,3)
            self.assertEqual(len(paginator.get_page(1)),3)
            self.assertEqual(len(paginator.get_page(2)),3)
            self.assertEqual(len(paginator.get_page(3)),3)
            
            
    def test_page_query_invalid_uses_page_1(self):
        response = self.client.get(reverse('recipe:home') + '?page=1A')
        self.assertEqual(response.context['recipes'].number,1)
        
        for i in range(9):
            kwargs = {
                'author_data': {'username' : f'u{i}'},
                'slug' : f'r{i}'
            }
            self.make_recipe(**kwargs)
            
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipe:home') + '?page=2')
            self.assertEqual(response.context['recipes'].number,2)
            

        

