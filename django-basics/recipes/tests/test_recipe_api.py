from unicodedata import category
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

    def test_recipe_api_list_do_not_show_not_published_recipe(self):
        recipe = self.make_recipe(
            is_published=False,title="Recipe not published",slug='recipe-published',author_data={"username":"author1"}
        )
        api_url = reverse("recipe:recipe_api-list")
        response = self.client.get(api_url)
        self.assertEqual(
            len(response.data.get("results")),
            0
        )

    def test_recipe_api_can_load_recipes_filtered_by_category(self):
        category_wanted = self.make_category("Category1")
        category_not_wanted = self.make_category("Category2")

        recipes = self.make_recipe_in_batch(qtd=5)

        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()
        recipes[0].category = category_not_wanted
        recipes[0].save()


        api_url = reverse("recipe:recipe_api-list") + f"?category_id={category_wanted.id}"

        response = self.client.get(api_url)
        self.assertEqual(
            len(response.data.get("results")),
            4
        )
