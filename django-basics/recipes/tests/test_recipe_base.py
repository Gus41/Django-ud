from django.test import TestCase
from recipes import views,models

class RecipeTestBase(TestCase):
     #Cria uma receita no banco de dados para cada teste 
     def setUp(self) -> None:
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
        return super().setUp()
    
