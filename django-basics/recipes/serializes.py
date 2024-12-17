from rest_framework import serializers
from recipes.models import Recipe, Category
from tags.models import Tag
from authors.validators import AuthorRecipeValidator
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class RecipeSerializer(serializers.ModelSerializer):
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)
    
    #category_name = serializers.StringRelatedField(source='category', read_only=True)
    tag_objects = TagSerializer(many=True, source='tags', read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipe:api_tag',
        read_only=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False
    )
    author = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all(),
        required=False
    )
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation',
            'tag_objects', 'tag_links',
            'preparation_time', 'preparation_time_unit', 'servings',
            'servings_unit',
            'preparation_steps', 'cover'
        ]
    def get_preparation(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"
    
    #validators
    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings
            
        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time       
            
        AuthorRecipeValidator(data=attrs,ErrorClass=serializers.ValidationError)
        
        return super().validate(attrs)
    
    def save(self, **kwargs):
        
        return super().save(**kwargs)

