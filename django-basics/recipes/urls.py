from recipes.views import home,recipe,category,search
from django.urls import path


app_name = 'recipe'
urlpatterns = [
    path('',home,name='home'),
    path('recipes/search/',search,name='search'),
    path('recipes/category/<int:id>', category,name='category'),
    path('recipes/<int:id>/',recipe,name='detail'),
]
