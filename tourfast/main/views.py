from django.shortcuts import render, get_object_or_404

from main.models import Hotel, Country, Tour


from django.shortcuts import render
from .models import Tour, Country

from django.shortcuts import render
from .models import Tour


def start(request):
    return render(request, 'main/start.html')

def cart(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    # Здесь логика работы с корзиной
    return render(request, 'cart.html', {'tour': tour})

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

def hotels(request):
    return render(request, 'main/hotels.html')

def sales(request):
    return render(request, 'main/sales.html')

def countries(request):
    return render(request, 'main/countries.html')