from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class RecipeCategoryModelTest(RecipeTestBase):
    
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Test_default'
        )
        return super().setUp()
    
    def test_recipe_category_model_string_representation_is_name_field(self):
        nedded = 'Test_default'
        self.category.name = nedded
        self.category.save()
        self.assertEqual(str(self.category), nedded)

    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError) as err:
            self.category.full_clean()
   

    
        
    