from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/',views.register, name='register'),
    path('create/',views.create, name='create'),
    path('login/',views.login, name='login'),
    path('recive_login/',views.recive_login, name='recive')
]
