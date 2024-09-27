from django.urls import reverse,resolve
from recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeDetailViewsTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipe:detail',kwargs={'id' : 1}))
        self.assertIs(view.func,views.recipe)


    def test_recipe_detail_view_returns_404(self):
        response = self.client.get(reverse('recipe:detail', kwargs={'id': 1000}))
        self.assertEqual(response.status_code,404)

    #--
    def test_recipe_detail_temaplte_loads_recipes(self):
        nedded_title = "Unique recipe"
        self.make_recipe(title=nedded_title)
        response = self.client.get(reverse('recipe:detail', kwargs={'id':1}))
        response_content = response.content.decode('utf-8')
        self.assertIn(nedded_title,response_content)

    def test_recipe_detail_temaplte_dont_load_recipes_not_published(self):
        nedded_title = 'This recipe will not apear'
        recipe = self.make_recipe(title=nedded_title,is_published=False)
        response = self.client.get(reverse('recipe:detail',kwargs={'id' : recipe.id}))       
        self.assertEqual(response.status_code,404)
