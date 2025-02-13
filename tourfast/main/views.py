from django.contrib.auth.decorators import login_required
from main.models import Hotel, Country, Tour, Buyer
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.views.generic import FormView
import requests
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def start(request):
    return render(request, 'main/start.html')

def tours(request):
    hotel = Hotel.objects.all()
    tour = Tour.objects.all()
    country = Country.objects.all()
    return render(request, 'main/tours.html', {'hotel': hotel, 'tour': tour, 'country': country})

def registration (request):

    first_name= Buyer.first_name
    last_name= Buyer.last_name
    email=Buyer.email
    password=Buyer.password
    password2=Buyer.password2
    print(first_name, last_name, email, password, password2)
    new_client = Buyer(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        password2=password2
    )
    new_client.save()

class registrationC (FormView):
    form_class = RegisterForm
    template_name = 'main/registration.html'
    success_url = reverse_lazy("login_page")
    def form_valid(self, form):
        form.save()
        registration(self.request)
        return super().form_valid(form)


def authorization(request):

    return render(request, 'main/authorization.html')

def hottours(request):
    return render(request, 'main/hottours.html')

def cart(request):
    return render(request, 'main/cart.html')

def profile(request):
    return render(request, 'main/profile.html')