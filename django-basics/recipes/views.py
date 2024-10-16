from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.http import HttpRequest,Http404
from django.db.models import Q
from recipes.models import Recipe
from django.core.paginator import Paginator
from utils import pagination
# Create your views here



def home(request : HttpRequest):
    recipes = Recipe.objects.all().filter(is_published=True).order_by('-id')
    paginator = Paginator(recipes,3)
    try:
        current_page = int(request.GET.get("page",1)) #if parameter page not exists, return 1
    except ValueError:
        current_page = 1
    
    page_obj = paginator.get_page(current_page)
    
    pagination_range = pagination.make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )
    context = {
        'recipes' : page_obj,
        'pagination_range' : pagination_range
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