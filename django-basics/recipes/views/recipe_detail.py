from django.views.generic import DetailView
from recipes.models import Recipe

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