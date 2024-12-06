from django.urls import reverse,resolve
from recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeSearchViewsTest(RecipeTestBase):
    #---------- search view
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipe:search'))
        self.assertIs(view.func.view_class,views.RecipeListViewSearch)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse("recipe:search") + '?q=teste')
        self.assertTemplateUsed(response,'recipes/pages/search.html')
        
    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse("recipe:search") + '?q=')
        self.assertEqual(response.status_code,404)

    def test_recipe_search_term_is_escaped(self):
        nedded = '<nedded>'
        response = self.client.get(reverse("recipe:search") + f'?q={nedded}')
        response_content = response.content.decode('utf-8')
        self.assertIn("&lt;nedded&gt;",response_content)

    def test_recipe_search_can_find_recipe_by_title(self):
        nedded_title = "testing recipe test"
        searched_title = "test"
        recipe = self.make_recipe(title=nedded_title,slug='testing-recipe-test')

        response = self.client.get(reverse("recipe:search") + f'?q={searched_title}')
        self.assertIn(recipe,response.context['recipes'])

    def test_recipe_search_can_find_recipe_by_descripion(self):
        nedded_description = "testing recipe test"
        searched_title = "test"
        recipe = self.make_recipe(description=nedded_description,slug='testing-recipe-test')

        response = self.client.get(reverse("recipe:search") + f'?q={searched_title}')
        self.assertIn(recipe,response.context['recipes'])
