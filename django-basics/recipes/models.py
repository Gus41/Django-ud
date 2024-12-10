from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify 
from tags.models import Tag
from django.contrib.contenttypes.fields import GenericRelation

class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.name
    
    
class RecipeManager(models.Manager):
    
    def get_recipes_publhised(self):
        return self.filter(
            is_published=True
        )

class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=20)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=20)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) # no momento da criação é gerada a data
    updated_at = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/',blank=True)
    #Relações
    category = models.ForeignKey(Category,default=None,on_delete=models.SET_NULL, null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = GenericRelation(Tag,related_query_name='recipes')

    def __str__(self) -> str:
        return self.title
    
    
    def get_absolute_url(self):
        return reverse("recipe:detail", args=(self.id,))
    
    def save(self,*args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug
            
            
        return super().save(*args, **kwargs)
    
    
