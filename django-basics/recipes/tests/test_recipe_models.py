from .test_recipe_base import RecipeTestBase,models
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeModelTest(RecipeTestBase):
    
    #Creating a recipe for all tests
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    

    @parameterized.expand([
        ('title',65),
        ('description',165),
        ('preparation_time_unit',65),
        ('servings_unit',65),
    ])
    def test_recipe_fields_max_length(self,field,max_length):
        setattr(self.recipe,field,'A' * (max_length+1))
        with self.assertRaises(ValidationError) as err:
            self.recipe.full_clean()

    def test_recipe_preparation_step_is_html_is_false_by_default(self):
        recipe = models.Recipe(
            category = self.make_category('Teste_default'),
            author=self.make_author(username="User_default"),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        self.assertFalse(recipe.preparation_steps_is_html, msg="Preparation Steps is Html is not false by default")

    def test_recipe_is_published_is_false_by_default(self):
        recipe = models.Recipe(
            category = self.make_category('Teste_default'),
            author=self.make_author(username="User_default"),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        self.assertFalse(recipe.is_published, msg="Is published is not false by default")