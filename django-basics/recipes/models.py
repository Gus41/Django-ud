from collections import defaultdict
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify 
from tags.models import Tag
import os
from django.conf import settings
from PIL import Image
from django.utils.text import slugify
import string
from random import SystemRandom


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.name
    
    
class RecipeManager(models.Manager):
    
    def get_recipes_publhised(self):
        return self.filter(
            is_published=False
        ).select_related('category','author').prefetch_related('tags')

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
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.title
    
    
    def get_absolute_url(self):
        return reverse("recipe:detail", args=(self.id,))
    
    @staticmethod
    def resize_image(img,new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pillow = Image.open(img_full_path)
        original_width, original_height = img_pillow.size
        
        if original_width <= new_width:
            img_pillow.close()
            return
        new_heigth = round((new_width * original_height) / original_width) # regra de 3
        
        new_img = img_pillow.resize((new_width,new_heigth,),Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=60
        )
        #print("resizing image")
    
    def save(self,*args, **kwargs):
        if not self.slug:
            rand_chars = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5
                )
            )
            self.slug = slugify(f'{self.title}-{rand_chars}')
            
       
            
        saved = super().save(*args, **kwargs)
        
        if self.cover:
            try:
                self.resize_image(self.cover)
            except FileNotFoundError:
                ...
        return saved
    
    def clean(self, *args, **kwargs):
        
        error_messages = defaultdict(list)
        
        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()
        
        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Recipe must have a unique title'
                )
        
        if error_messages:
            raise ValidationError(error_messages)
        
        return super().clean()
    
