import os
from django.views.generic import ListView
from recipes.models import Recipe
from utils import pagination
from django.http import Http404
from django.db.models import Q
from django.http import JsonResponse


PER_PAGE = os.environ.get("PER_PAGE")

class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    paginate_by = None
    
    def get_queryset(self,*args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)

        query_set = query_set.filter(
            is_published = True
        )
        query_set = query_set.prefetch_related("author","category")
        return query_set
    
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        
        page_obj,pagination_range,current_page = pagination.make_pagination(self.request,context_data.get("recipes"),PER_PAGE)
        context_data.update({
            'recipes' : page_obj,
            'pagination_range' : pagination_range,
            'current_page':current_page
        })
        return context_data
    
    
class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'
      
class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'
    
    def get_queryset(self,*args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)

        query_set = query_set.filter(
            is_published = True,
            category__id = self.kwargs.get("id") 
        )
        
        if not query_set:
            raise Http404()
        
        return query_set
    
    
class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'
    
    
    def get_queryset(self,*args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        term = self.request.GET.get("q",'')
        if not term:
            raise Http404()
        query_set = query_set.filter(
            Q(
                Q(title__icontains=term) | Q(description__icontains=term) # OR
            ), 
        is_published=True
            
        )
        
        return query_set

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        term = self.request.GET.get("q",'')

        page_obj,pagination_range,current_page = pagination.make_pagination(self.request,context_data.get("recipes"),PER_PAGE)
        context_data.update({
            'recipes' : page_obj,
            'pagination_range' : pagination_range,
            'current_page' : current_page,
            'term' : term,
            'aditional_url_query' : f'&q={term}'
        })
        return context_data
    
    
    
class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'
    
    def render_to_response(self, context, **response_kwargs):
        recipes = list(self.get_context_data()['recipes'].object_list.values()) 
        
        return JsonResponse(recipes, safe=False)



    