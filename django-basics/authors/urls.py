from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/',views.register, name='register'),
    path('create/',views.create, name='create'),
    path('login/',views.login_view, name='login'),
    path('recive_login/',views.recive_login, name='recive'),
    path('logout/',views.logout_view, name='logout'),
    path('dashboard/',views.dashboard, name="dashboard"),
    path('dashboard/<int:id>/edit/',views.DashBoardRecipe.as_view(),name='dashboard_recipe'),
    path('dashboard/recipe/create',views.DashBoardRecipe.as_view(),name="create_recipe"),
    path('dashboard/delete',views.DashBoardDeleteRecipe.as_view(),name="delete_recipe"),
]
