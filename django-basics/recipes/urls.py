from recipes.views import home,recipe
from django.urls import path



urlpatterns = [
    path('',home),
    path('recipes/<int:id>/',recipe)
]