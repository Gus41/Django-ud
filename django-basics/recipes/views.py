from django.shortcuts import render
from django.http import HttpRequest
from utils.main import make_recipe
from recipes.models import Recipe
# Create your views here.


def home(request : HttpRequest):
    recipes = Recipe.objects.all().order_by('-id')
    context = {
        'recipes' : recipes
    }
    return render(request,'recipes/pages/home.html',context)

def recipe(request: HttpRequest, id : int):
    context = {
        'recipe': make_recipe(),
        'is_detail' : True
    }
    return render(request,'recipes/pages/recipe-detail.html',context)
