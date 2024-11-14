from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.http import HttpRequest,Http404
from django.db.models import Q
from recipes.models import Recipe
from django.core.paginator import Paginator
from utils import pagination
from django.contrib import messages
import os

# Create your views here

PER_PAGE = os.environ.get("PER_PAGE")

def home(request : HttpRequest):
   
    recipes = Recipe.objects.all().filter(is_published=True).order_by('-id')    
    page_obj,pagination_range,current_page = pagination.make_pagination(request,recipes,PER_PAGE)
    
    messages.success(request,"Succes")
    context = {
        'recipes' : page_obj,
        'pagination_range' : pagination_range,
        'current_page' : current_page
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
    page_obj,pagination_range,current_page = pagination.make_pagination(request,recipes,PER_PAGE)
    context = {
        'recipes' : page_obj,
        'pagination_range' : pagination_range,
        'current_page' : current_page,
        'title' : f'{recipes[0].category.name}'
    }

    return render(request,'recipes/pages/category.html',context)

def search(request : HttpRequest):
    messages.success(request,"Pesquisa efetuada")
    term = request.GET.get("q",'').strip()

    if not term:
        raise Http404
    
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=term) | Q(description__icontains=term) # OR
        ), 
        is_published=True
    ).order_by("-id")

    page_obj,pagination_range,current_page = pagination.make_pagination(request,recipes,PER_PAGE)
    context = {
        'recipes' : page_obj,
        'pagination_range' : pagination_range,
        'current_page' : current_page,
        'term' : term,
        'aditional_url_query' : f'&q={term}'
    }

    return render(request,'recipes/pages/search.html',context)