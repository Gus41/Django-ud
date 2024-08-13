from recipes.views import home,recipe
from django.urls import path


app_name = 'recipe'
urlpatterns = [
    path('',home,name='home'),
    path('recipes/<int:id>/',recipe,name='detail')
]