from recipes.views import RecipeListViewHome,RecipeListViewCategory,RecipeListViewSearch,RecipeDetail,RecipeListViewHomeApi,RecipeDetailApi, Theory,RecipeListViewTags,recipe_list,recipe
from django.urls import path


app_name = 'recipe'
urlpatterns = [
    path('',RecipeListViewHome.as_view(),name='home'),
    path('recipes/search/',RecipeListViewSearch.as_view(),name='search'),
    path('recipes/category/<int:id>', RecipeListViewCategory.as_view(),name='category'),
    path('recipes/<int:pk>/',RecipeDetail.as_view(),name='detail'),
    
    path('recipes/api/v1',RecipeListViewHomeApi.as_view(),name='recipesapi'),
    path('recipes/api/v1/<int:pk>',RecipeDetailApi.as_view(),name='recipesapi'),
     
     #--
     path("recipes/theory/",Theory,name='theory'),
     path("recipes/tags/<slug:slug>",RecipeListViewTags.as_view(),name='tags'),
     
     #api
     path(
         'api/recipes/',
         recipe_list,
         name='api_recipes'
     ),
     path(
         'api/recipes/<int:pk>',
         recipe,
         name='api_recipes'
     ),
     
]
