from django.urls import reverse,resolve
from recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeCategoryViewsTest(RecipeTestBase):
   
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipe:category', kwargs={'id' : 1}))
        self.assertIs(view.func.view_class,views.RecipeListViewCategory)
        
    def test_recipe_category_temaplte_dont_load_recipes_not_published(self):
        nedded_title = 'This recipe will not apear'
        recipe = self.make_recipe(title=nedded_title,is_published=False)
        response = self.client.get(reverse('recipe:category',kwargs={'id' : recipe.category.id}))       
        self.assertEqual(response.status_code,404)

    def test_recipe_category_view_returns_404(self):
        response = self.client.get(reverse('recipe:category', kwargs={'id': 1000}))
        self.assertEqual(response.status_code,404)


    def test_recipe_category_temaplte_loads_recipes(self):
        nedded_category = 'Category-test'
        nedded_title = 'Recipe created in this Category-test'
        self.make_recipe(category_data={'name':nedded_category},title=nedded_title)
        response = self.client.get(reverse('recipe:category', kwargs={'id':1}))
        response_content = response.content.decode('utf-8')
        self.assertIn(nedded_title,response_content)
        self.assertIn(nedded_category,response_content)
        
    
