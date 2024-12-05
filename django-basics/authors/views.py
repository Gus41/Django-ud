from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.http import HttpRequest,Http404
from django.contrib import messages
from django.urls import reverse

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
        raise Http404

    POST = request.POST

    request.session["register_form_data"] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password) # hash pass
        user.save()
        
        messages.success(request,"User created!")
        del(request.session["register_form_data"])

    return redirect('auth:register')
