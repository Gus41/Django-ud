from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

# Create your views here.


def home(request : HttpRequest):
    return render(request,'recipes/pages/home.html', context={
        'name' : 'Teste'
    })

def recipe(request: HttpRequest, id : int):
    
    return render(request,'recipes/pages/recipe-detail.html',context={
        'teste' : 'teste'
    })
