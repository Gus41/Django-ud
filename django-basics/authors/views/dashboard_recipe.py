from django.views import View
from recipes.models import Recipe
from authors.forms import AuthorRecipeForm
from django.contrib import messages
from django.http import HttpRequest,Http404
from django.urls import reverse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(
    login_required(login_url='auth:login', redirect_field_name='next'),
    name='dispatch'
)
class DashBoardRecipe(View):
    
    
    def get_recipe(self,id: int):
        
        recipe = None
        
        if id:
            recipe = Recipe.objects.filter(
                pk=id
            ).first()
            
            if not recipe:
                raise Http404

        return recipe

    def render_recipe(self,context):
        return render(self.request,"author/pages/dashboard_recipe.html",context)
    
   
    def get(self, request: HttpRequest, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        
        if id is not None:
            form_action = reverse("auth:dashboard_recipe", args=(id,))
        else:
            form_action = reverse("auth:create_recipe") 
        
        context = {
            'recipe': recipe,
            'form': form,
            'form_action': form_action,
        }
        return self.render_recipe(context)

    
    def post(self, request: HttpRequest, id: int | None = None):
        
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(data=request.POST or None, files=request.FILES or None, instance=recipe)
        
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            
            recipe.save()
            messages.success(request, "Recipe saved")
            return redirect(reverse("auth:dashboard_recipe", args=(recipe.id,)))
        
        
        form_action = reverse("auth:create_recipe")
        # if has an id user is editing a recipe, else he is creating a new recipe
        if id is not None:
            form_action = reverse("auth:dashboard_recipe", args=(id,))
        
        context = {
            'recipe': recipe,
            'form': form,
            'form_action': form_action
        }
        return self.render_recipe(context)
    
@method_decorator(
    login_required(login_url='auth:login', redirect_field_name='next'),
    name='dispatch'
)
class DashBoardDeleteRecipe(DashBoardRecipe):
    def post(self,*args, **kwargs):
        
        recipe = self.get_recipe(self.request.POST.get("id"))
        recipe.delete()
        messages.success(self.request,"Recipe deleted")
        return redirect(reverse("auth:dashboard"))

        