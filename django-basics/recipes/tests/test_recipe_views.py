from django.urls import reverse,resolve
from recipes import views,models
from .test_recipe_base import RecipeTestBase
from unittest import skip

class RecipeViewsTest(RecipeTestBase):

    
    #vai ser executado depois cada um dos testes
    def tearDown(self) -> None:
        return super().tearDown()    
    

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

    #----------- template tests
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipe:home'))
        self.assertTemplateUsed(response,'recipes/pages/home.html')


    #t----------- estando se a home renderiza no recipes founded
    def test_recipe_homes_template_show_no_recipes_founded_if_no_recipes(self):
        
        response = self.client.get(reverse('recipe:home'))
        self.assertIn('No recipes found...',response.content.decode('utf-8'))

    #---------- status code view 404 (getobjector404)
    def test_recipe_category_view_returns_404(self):
        response = self.client.get(reverse('recipe:category', kwargs={'id': 1000}))
        self.assertEqual(response.status_code,404)

    def test_recipe_detail_view_returns_404(self):
        response = self.client.get(reverse('recipe:detail', kwargs={'id': 1000}))
        self.assertEqual(response.status_code,404)
        
    #---------
    def test_recipe_home_temaplte_loads_recipes(self):
        nedded_title = 'Recipe created'
        self.make_recipe(title=nedded_title)
        response = self.client.get(reverse('recipe:home'))
        response_content = response.content.decode('utf-8')
       
        self.assertIn(nedded_title,response_content)
        #self.fail('Falhar teste por n motivos')

    def test_recipe_category_temaplte_loads_recipes(self):
        nedded_category = 'Category-test'

        nedded_title = 'Recipe created in this Category-test'
        
        self.make_recipe(category_data={'name':nedded_category},title=nedded_title)

        response = self.client.get(reverse('recipe:category', kwargs={'id':1}))
        response_content = response.content.decode('utf-8')
        self.assertIn(nedded_title,response_content)
        self.assertIn(nedded_category,response_content)
        
    
    def test_recipe_detail_temaplte_loads_recipes(self):
        nedded_title = "Unique recipe"
        self.make_recipe(title=nedded_title)
        response = self.client.get(reverse('recipe:detail', kwargs={'id':1}))
        response_content = response.content.decode('utf-8')
        self.assertIn(nedded_title,response_content)

    
        