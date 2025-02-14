from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import FormView, CreateView
from rest_framework.reverse import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from main.models import Hotel, Country, Tour, Buyer
from .forms import RegisterForm, LoginForm
from django.shortcuts import render

from .forms import RegisterForm
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

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'main/registration.html'
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user = form.save(commit=False)  # Создаём, но не сохраняем сразу
        user.set_password(form.cleaned_data['password1'])  # Хешируем пароль
        user.save()  # Теперь сохраняем

        login(self.request, user)  # Логиним пользователя
        return super().form_valid(form)


class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'main/authorization.html'

    def get_success_url(self):
        return reverse_lazy("profile")

def authorization(request):
    return render(request, 'main/authorization.html')

def hottours(request):
    return render(request, 'main/hottours.html')

def cart(request):
    return render(request, 'main/cart.html')

@login_required
def profile(request):
    return render(request, 'main/profile.html')