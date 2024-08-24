from django.shortcuts import render
from django.http import HttpRequest
from utils.main import make_recipe
from recipes.models import Recipe,Category
# Create your views here.


def home(request : HttpRequest):
    recipes = Recipe.objects.all().filter(is_published=True).order_by('-id')
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


def category( request: HttpRequest, id: int):
    recipes  = Recipe.objects.filter(is_published=True).filter(category__id=id)
    context = {
        'recipes' : recipes
    }
    return render(request,'recipes/pages/category.html',context)
