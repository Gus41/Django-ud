from recipes.views import RecipeListViewHome,RecipeListViewCategory,RecipeListViewSearch,RecipeDetail
from django.urls import path


app_name = 'recipe'
urlpatterns = [
    path('',RecipeListViewHome.as_view(),name='home'),
    path('recipes/search/',RecipeListViewSearch.as_view(),name='search'),
    path('recipes/category/<int:id>', RecipeListViewCategory.as_view(),name='category'),
    path('recipes/<int:pk>/',RecipeDetail.as_view(),name='detail'),
]
