from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/',views.register, name='register'),
    path('create/',views.create, name='create'),
    path('login/',views.login_view, name='login'),
    path('recive_login/',views.recive_login, name='recive'),
    path('logout/',views.logout_view, name='logout')
]
