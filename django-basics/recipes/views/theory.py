from django.shortcuts import render
from recipes.models import Recipe
from django.db.models import Q,Value,F
from django.db.models.functions import Concat

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
    )[:10].annotate(
        author_full_name=Concat(F("author__first_name"), Value(" "), F("author__last_name"))
    )
    
    
    context = {
        'recipes': recipes
    }
    return render(
        request,'recipes/pages/theory.html',
        context
    )
    
    