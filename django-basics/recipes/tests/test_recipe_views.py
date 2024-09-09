from django.test import TestCase
from django.urls import reverse,resolve
from recipes import views,models


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
        category = models.Category.objects.create(name="catecoty_mock")
        author = models.User.objects.create_user(
            first_name='user',
            last_name='user',
            password='user',
            email='user@gmail.com',
            username='user'
        )
        recipe = models.Recipe.objects.create(
            category=category,
            author=author,
            title = 'Recipe',
            description = 'Description',
            slug = 'recipe-slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutes',
            servings = 5,
            servings_unit = 'Porções',
            preparation_steps = 'lorem',
            preparation_steps_is_html = False,
            updated_at = '',
            is_published = True,
            
            )
        response = self.client.get(reverse('recipe:home'))
        response_content = response.content.decode('utf-8')
        self.assertIn(recipe.description,response_content)
        self.assertIn(recipe.servings_unit,response_content)
        self.assertIn(recipe.title,response_content)
        
        