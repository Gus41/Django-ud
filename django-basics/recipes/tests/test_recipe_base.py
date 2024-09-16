from django.test import TestCase
from recipes import models

class RecipeTestBase(TestCase):
     #Cria uma receita no banco de dados para cada teste 

    def setUp(self) -> None:

        category = self.make_category('Teste')
        author = self.make_author('Fulano')
        self.make_recipe(category=category,author=author)
        return super().setUp()
    

    def make_category(self,name='Category'):
         return models.Category.objects.create(name=name)
    def make_author(self,name='user'):
        return models.User.objects.create_user(
            first_name=name,
            last_name=name,
            password='12345678',
            email='user@gmail.com',
            username=name
        )
    def make_recipe(self,category,author):
        return models.Recipe.objects.create(
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
    
    
