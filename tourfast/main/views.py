from django.shortcuts import render

# Create your views here.

def start(request):
    return render(request, 'main/start.html')

def tours(request):
    return render(request, 'main/tours.html')

def registration(request):
    return render(request, 'main/registration.html')

def authorization(request):
    return render(request, 'main/authorization.html')

def hottours(request):
    return render(request, 'main/hottours.html')

def cart(request):
    return render(request, 'main/cart.html')

def profile(request):
    return render(request, 'main/profile.html')