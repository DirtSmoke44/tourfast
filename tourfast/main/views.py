
from django.shortcuts import render, get_object_or_404
from main.models import Hotel, Country, Tour



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import FormView, CreateView
from rest_framework.reverse import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from main.models import Hotel, Country, Tour, Buyer
from .forms import RegisterForm, LoginForm

from django.shortcuts import render
from django.contrib.auth import logout
from .forms import RegisterForm
from .models import Tour, Country
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Tour
from .filters import TourFilter
from .forms import CustomTourFilterForm

def logout_view(request):
    logout(request)
    return redirect("start_page")

def start(request):
    return render(request, 'main/start.html')

@login_required
def cart(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    # Здесь логика работы с корзиной

    return render(request, 'cart.html', {'tour': tour})

def tours(request):
    hotel = Hotel.objects.all()
    tours = Tour.objects.all()
    country = Country.objects.all()
    tour_filter = TourFilter(request.GET, queryset=Tour.objects.all())
    if request.GET:
        form = CustomTourFilterForm(request.GET)

        if form.is_valid():
            # Применяем фильтры вручную
            if form.cleaned_data['country']:
                tours = tours.filter(country=form.cleaned_data['country'])
            if form.cleaned_data['price_min']:
                tours = tours.filter(price__gte=form.cleaned_data['price_min'])
            if form.cleaned_data['price_max']:
                tours = tours.filter(price__lte=form.cleaned_data['price_max'])
            if form.cleaned_data['duration_min']:
                tours = tours.filter(duration__gte=form.cleaned_data['duration_min'])
            if form.cleaned_data['duration_max']:
                tours = tours.filter(duration__lte=form.cleaned_data['duration_max'])
    else:
        form = CustomTourFilterForm()

    return render(request, 'main/tours.html', {'form': form,'hotel': hotel, 'tour': tours, 'country': country, 'filter': tour_filter})


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

def hotels(request):
    hotel = Hotel.objects.all()
    return render(request, 'main/hotels.html', {'hotel': hotel})

def sales(request):
    return render(request, 'main/sales.html')

def countries(request):
    country = Country.objects.all()
    return render(request, 'main/countries.html', {'country': country})

def orderaccept(request):
    return render(request, 'main/orderaccept.html')

def reservation(request):
    return render(request, 'main/reservation.html')

