from django.shortcuts import redirect, render
from .forms import RegisterForm,LoginForm,AuthorRecipeForm
from django.http import HttpRequest,Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe

def register(request: HttpRequest):

    register_form_data = request.session.get("register_form_data") or None

    form = RegisterForm(register_form_data)
    context = {
        'form' : form,
        'form_action': reverse('auth:create')
    }
    return render(request,'author/pages/register_view.html',context)

#---------------------------------------------
def create(request: HttpRequest):
    if not request.POST:
        raise Http404()

    POST = request.POST

    request.session["register_form_data"] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password) # hash pass
        user.save()
        
        messages.success(request,"User created!")
        del(request.session["register_form_data"])
        return redirect(reverse('auth:login'))

    return redirect(reverse('auth:register'))

#---------------------------

def login_view(request: HttpRequest):
    form = LoginForm()
    context = {
        'form': form,
        'form_action': reverse('auth:recive'),
    }
    return render(request, 'author/pages/login.html', context)

def recive_login(request: HttpRequest):
    if request.method != "POST":
        raise Http404()
    
    form = LoginForm(request.POST)
    initial = reverse("recipe:home")
    
    if form.is_valid():
        authenticate_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get("password", ''),
        )
        if authenticate_user is not None:
            login(request, authenticate_user)  
            messages.success(request, "You are Logged In!")
            return redirect(reverse("recipe:dashboard"))
        else:
            messages.error(request, "Invalid credentials")
    else:
        messages.error(request, "Invalid data")
    return redirect(initial)

@login_required(login_url='auth:login', redirect_field_name='next')
def logout_view(request: HttpRequest):
    if not request.POST:
        raise Http404()
    
    if request.POST.get("username") != request.user.username:
        return redirect(reverse("auth:login"))
        
        
    logout(request)
    messages.success(request,"You are loged out")
    return redirect(reverse("auth:login"))


@login_required(login_url='auth:login', redirect_field_name='next')
def dashboard(request: HttpRequest):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    context = {
        'recipes': recipes
    }
    return render(request,"author/pages/dashboard.html",context)


@login_required(login_url='auth:login', redirect_field_name='next')
def dashboard_recipe(request: HttpRequest, id: int):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()
    
    if not recipe:
        raise Http404()
    
    form = AuthorRecipeForm(data=request.POST or None,files=request.FILES or None,instance=recipe)
    
    
    if form.is_valid():
        _recipe = form.save(commit=False)
        _recipe.author = request.user
        _recipe.preparation_steps_is_html = False
        
        _recipe.save()
        messages.success(request,"Recipe saved")
        return redirect(reverse("auth:dashboard_recipe", args=(id,)))
    
    context = {
        'recipe': recipe,
        'form': form,
        'form_action': reverse("auth:dashboard_recipe", args=(id,))
    }
    return render(request,"author/pages/dashboard_recipe.html",context)

@login_required(login_url='auth:login', redirect_field_name='next')
def dashboard_create(request: HttpRequest):
    
    form = AuthorRecipeForm(data=request.POST or None,files=request.FILES or None)
    
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.is_published = False
        recipe._preparation_steps_is_html = False
        recipe.author = request.user
        id = recipe.pk
        
        recipe.save()
        messages.success(request,"Recipe created")
        return redirect(reverse("auth:dashboard_recipe", args=(id,)))
        
    context = {
        'form': form,
        'form_action': reverse('auth:create_recipe')
    }
    
    return render(request,"author/pages/dashboard_recipe.html",context)


@login_required(login_url='auth:login', redirect_field_name='next')
def dashboard_delete_recipe(request: HttpRequest):
    
    if not request.POST:
        raise Http404()
    
    id = request.POST.get("id")
    
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()
    
    if not recipe:
        raise Http404()
    
    recipe.delete()
    messages.success(request,"Recipe deleted")
    return redirect(reverse("auth:dashboard"))


