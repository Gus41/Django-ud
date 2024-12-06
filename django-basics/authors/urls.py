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
    path('dashboard/<int:id>/edit/',views.dashboard_recipe,name='dashboard_recipe'),
    path('dashboard/recipe/create',views.dashboard_create,name="create_recipe"),
    path('dashboard/delete',views.dashboard_delete_recipe,name="delete_recipe"),
]
