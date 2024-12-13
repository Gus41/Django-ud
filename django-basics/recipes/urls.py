from recipes.views import *
from django.urls import path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('api/recipes',RecipeApi,basename='recipe_api')



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
     
     path(
         'api/tag/<int:pk>',
         tag,
         name='api_tag'
     ),
     
]
urlpatterns += router.urls
