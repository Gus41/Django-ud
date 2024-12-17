from recipes.views import *
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)



app_name = 'recipe'

router = SimpleRouter()
router.register('api/recipes',RecipeApi,basename='recipe_api')

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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


     
]
urlpatterns += router.urls
