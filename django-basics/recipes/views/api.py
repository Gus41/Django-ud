from django.http import HttpResponse,HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe,Tag
from recipes.serializes import RecipeSerializer,TagSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status


@api_view(http_method_names=['get','post'])
def recipe_list(request: HttpRequest):
    if request.method == 'GET':
        recipes = Recipe.objects.get_recipes_publhised()
        serializer = RecipeSerializer(instance=recipes,many=True,context={'request':request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view(http_method_names=['get','patch','delete'])
def recipe(request,pk):
    recipe = get_object_or_404(
            Recipe.objects.get_recipes_publhised(),
            pk=pk
        )
    if request.method == 'GET':
        serializer = RecipeSerializer(instance=recipe)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = RecipeSerializer(instance=recipe,data=request.data,context={'request':request},partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view()
def tag(request,pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(tag)
    return Response(serializer.data)
