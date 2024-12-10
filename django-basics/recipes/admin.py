from django.contrib import admin
from .models import Category,Recipe
from django.contrib.contenttypes.admin import GenericStackedInline
from tags.models import Tag
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    ...
    
class TagInline(GenericStackedInline):
    model = Tag

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_at','is_published')
    list_display_links = ('title',)
    search_fields = ('id','title','description',)
    list_filter = ('is_published','preparation_steps_is_html','category','author',)
    list_per_page = 10
    list_editable = ('is_published',)
    ordering = ('-id',)
    
    prepopulated_fields = {
        'slug':('title',)
    }
    inlines = [
        TagInline,
    ]

    
    
admin.site.register(Category,CategoryAdmin)
admin.site.register(Recipe,RecipeAdmin)