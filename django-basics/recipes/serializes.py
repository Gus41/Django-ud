from rest_framework import serializers
from recipes.models import Recipe

class RecipeSerializer(serializers.Serializer):
    #fields
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)