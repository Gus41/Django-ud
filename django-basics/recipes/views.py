from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.http import HttpRequest,Http404
from django.db.models import Q
from recipes.models import Recipe
from django.core.paginator import Paginator
# Create your views here

def home(request : HttpRequest):
    recipes = Recipe.objects.all().filter(is_published=True).order_by('-id')
    context = {
        'recipes' : recipes
    }
    return render(request,'recipes/pages/home.html',context)

def recipe(request: HttpRequest, id : int):
    recipe = get_object_or_404(Recipe,id=id,is_published=True)

    context = {
        'recipe': recipe,
        'is_detail' : True
    }
    return render(request,'recipes/pages/recipe-detail.html',context)


def category( request: HttpRequest, id: int):
    recipes = get_list_or_404(Recipe.objects.filter(category__id=id,is_published=True).order_by('-id'))
    #----
    context = {
        'recipes' : recipes,
        'title' : f'{recipes[0].category.name}'
    }
    return render(request,'recipes/pages/category.html',context)

def search(request : HttpRequest):
    term = request.GET.get("q",'').strip()

    if not term:
        raise Http404
    
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=term) | Q(description__icontains=term) # OR
        ), 
        is_published=True
    ).order_by("-id")

    context = {
        'recipes' : recipes,
        'term' : term
    }
    return render(request,'recipes/pages/search.html',context)