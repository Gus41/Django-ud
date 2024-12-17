from django.urls import reverse
from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from unittest.mock import patch



class RecipeApiTest(test.APITestCase,RecipeMixin):
    
    def test_recipe_api_list_returns_200(self):
        api_url = reverse("recipe:recipe_api-list")
        response = self.client.get(api_url)
        
        self.assertEqual(response.status_code,200)

    @patch('recipes.views.api.RecipeApiPagination.page_size',new=2)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_recipes = 10
        self.make_recipe_in_batch(qtd=wanted_recipes)
        api_url = reverse("recipe:recipe_api-list")
        response = self.client.get(api_url)
        recipes_received = len(response.data.get("results"))
        self.assertEqual(
            2,
            recipes_received
        )