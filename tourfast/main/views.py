from django.shortcuts import render

from main.models import Hotel, Country, Tour


from django.shortcuts import render
from .models import Tour, Country

from django.shortcuts import render
from .models import Tour


def start(request):
    return render(request, 'main/start.html')

def tours(request):
    hotel = Hotel.objects.all()
    tour = Tour.objects.all()
    country = Country.objects.all()
    return render(request, 'main/tours.html', {'hotel': hotel, 'tour': tour, 'country': country})

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