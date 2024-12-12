from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe
from recipes.serializes import RecipeSerializer
from django.shortcuts import get_object_or_404


@api_view()
def recipe_list(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(instance=recipes,many=True)
    
    return Response(serializer.data)


@api_view()
def recipe(request,pk):
    recipe = get_object_or_404(
        Recipe.objects.all(),
        pk=pk
    )
    serializer = RecipeSerializer(instance=recipe)
    
    return Response(serializer.data)
