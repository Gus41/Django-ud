from django.shortcuts import render
from django.http import HttpRequest
from utils.main import make_recipe
# Create your views here.


def home(request : HttpRequest):
    context = {
        'recipes' : [make_recipe() for _ in range(10)]
    }
    return render(request,'recipes/pages/home.html',context)

def recipe(request: HttpRequest, id : int):
    context = {
        'recipe': make_recipe()
    }
    return render(request,'recipes/pages/recipe-detail.html',context)
