from django.views.generic import DetailView
from recipes.models import Recipe
from django.http import JsonResponse
from django.forms.models import model_to_dict


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data.update({
            'is_detail' : True,
        })
        return context_data
    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(
            is_published=True
        )
        return query_set
    
    
    
class RecipeDetailApi(RecipeDetail):
    
    def render_to_response(self, context, **response_kwargs):
        recipe_model = self.get_context_data()['recipe']
        recipe = model_to_dict(recipe_model)
        
        
        recipe['created_at'] = str(recipe_model.created_at)
        recipe['updated_at'] = str(recipe_model.updated_at)
        
        if recipe.get('cover'):
            recipe['cover'] = self.request.build_absolute_uri() + recipe['cover']
        else:
            recipe['cover'] = ''
        
        return JsonResponse(recipe, safe=False)
