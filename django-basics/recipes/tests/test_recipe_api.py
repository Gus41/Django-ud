from tarfile import data_filter
from urllib import response
from django.urls import reverse
from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from unittest.mock import patch



class RecipeApiTest(test.APITestCase,RecipeMixin):

    def get_auth_data(self):
        userdata={
            'username': 'user',
            'password': 'password123'
        }
        user = self.make_author(username=userdata.get("username"),password=userdata.get("password"))

        response = self.client.post(path=reverse('recipe:token_obtain_pair'),data=userdata)
        
        return {
            **response.data,
            "user": user
        }
    
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
    def test_recipe_api_list_user_must_send_jwt_to_create_recipe(self):
        api_url = reverse("recipe:recipe_api-list")
        response = self.client.post(api_url)
        self.assertEqual(response.status_code,401)


    def test_recipe_api_logged_users_can_create_recipe(self):
        data={
            "title":"This is the title",
            "description": "description",
            "preparation_time":1,
            "preparation_time_unit": "Minute",
            "servings":1,
            "servings_unit":"Person",
            "preparation_steps": "preparation steps"
        }

        response = self.client.post(
            reverse("recipe:recipe_api-list"),
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.get_auth_data().get("access")}'
            )
        
        self.assertEqual(
            response.status_code,
            201
        )


    def test_recipe_api_logged_users_can_update_recipe(self):
        auth_data = self.get_auth_data()
        recipe = self.make_recipe()
        recipe.author = auth_data.get("user")
        recipe.save()


        new_title = "Diferent Title 123"
        response = self.client.patch(
            reverse("recipe:recipe_api-detail",args=(recipe.id,)),
            data={"title":new_title},
            HTTP_AUTHORIZATION=f'Bearer {auth_data.get("access")}'
            )

        self.assertEqual(
            response.data.get("title"),
            new_title
        )


    def test_recipe_api_logged_users_cant_update_owned_by_another_user(self):
        auth_data = self.get_auth_data()
        recipe = self.make_recipe()
        recipe.save()


        new_title = "Diferent Title 123"
        response = self.client.patch(
            reverse("recipe:recipe_api-detail",args=(recipe.id,)),
            data={"title":new_title},
            HTTP_AUTHORIZATION=f'Bearer {auth_data.get("access")}'
            )

        self.assertEqual(
            response.status_code,
            403
        )    
