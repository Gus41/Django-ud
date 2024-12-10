from django.shortcuts import render
from recipes.models import Recipe
from django.db.models import Q


def Theory(request, *args, **kwargs):
    
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains='da',
              id__gt=2,
              is_published=True,) |
            Q(
                id__gt=1000
            )
        )
    )[:10]
    
    context = {
        'recipes': recipes
    }
    return render(
        request,'recipes/pages/theory.html',
        context
    )
    
    