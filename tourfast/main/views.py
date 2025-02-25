
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
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tour
import logging
logger = logging.getLogger(__name__)



from django.shortcuts import render

def logout_view(request):
    logout(request)
    return redirect("start_page")

def start(request):
    return render(request, 'main/start.html')



@login_required
def cart_page(request):
    cart = request.session.get('cart', {'tours': []})
    print(f"Текущая корзина: {cart}")  # Отладочный вывод
    tour_ids = cart.get('tours', [])
    tours = Tour.objects.filter(id__in=tour_ids)
    hotel_price = sum(tours.hotel.price_per_night for tours in tours)
    total_price = sum(tours.price for tours in tours)
    return render(request, 'main/cart.html', {'tours': tours,
        'total_price': total_price, 'hotel_price': hotel_price})

@login_required
def add_to_cart(request, tour_id):
    print(f"Добавление тура {tour_id} в корзину")
    if 'cart' not in request.session:
        request.session['cart'] = {'tours': []}
        print("Корзина инициализирована")

    cart = request.session['cart']
    cart.setdefault('tours', [])

    if tour_id not in cart['tours']:
        cart['tours'].append(tour_id)
        print(f"Тур {tour_id} добавлен в корзину")

    request.session['cart'] = cart
    request.session.modified = True
    request.session.save()
    print(f"Текущая корзина: {cart}")

    return redirect('cart_page')



@login_required
def remove_from_cart(request, tour_id):
    """Удаляет тур из корзины."""
    cart = request.session.get('cart', {'tours': []})

    if tour_id in cart['tours']:
        cart['tours'].remove(tour_id)

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_page')


@login_required
def clear_cart(request):
    """Очищает корзину."""
    request.session['cart'] = {'tours': []}
    request.session.modified = True

    return redirect('cart_page')


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

def clearcart(request):
    return render(request, 'main/clear_cart.html')

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

def ordercomplete(request):
    return render(request, 'main/ordercomplete.html')

def reservation(request):
    return render(request, 'main/reservation.html')

def editprofile(request):
    return render(request, 'main/editprofile.html')

def contracts(request):
    return render(request, 'main/contracts.html')

