from recipes.views import home,recipe,category
from django.urls import path


app_name = 'recipe'
urlpatterns = [
    path('',home,name='home'),
    path('recipes/category/<int:id>', category,name='category'),
    path('recipes/<int:id>/',recipe,name='detail'),
]