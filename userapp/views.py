from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

def homePage(request):
    return render(request, "home.html")

@login_required

def productsPage(request):
    return render(request, "products.html")

def exit(request):
    logout(request)
    return redirect('home')
    