from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError

class RecipeModelTest(RecipeTestBase):
    
    #Creating a recipe for all tests
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 66
        
        with self.assertRaises(ValidationError) as err:
            self.recipe.full_clean()
        
    def test_recipe_fields_max_length(self):
        fields = [
            ('title',65),
            ('description',165),
            ('preparation_time_unit',65),
            ('servings_unit',65),
        ]

        for field in fields:
            ...