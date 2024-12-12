from rest_framework import serializers
from recipes.models import Recipe,Category
from tags.models import Tag
from django.contrib.auth.models import User


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField()
    
    
    

class RecipeSerializer(serializers.Serializer):
    #fields
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all()
    )
    category_name = serializers.StringRelatedField(
        source='category'
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset = Tag.objects.all(),
        many=True
    )
    tag_objects = TagSerializer(
        many=True,
        source='tags'
    )
    def get_preparation(self,recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
    
    
