from main.models import Hotel, Country, Tour, Contracts, Buyer, Transaction
from django.views.generic import FormView, CreateView
from rest_framework.reverse import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm
from django.contrib.auth import logout
from .filters import TourFilter
from .forms import CustomTourFilterForm, UserEditForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger(__name__)



def logout_view(request):
    logout(request)
    return redirect("start_page")

def start(request):
    tours = Tour.objects.filter(old_price__isnull=False)  # Фильтруем только те, у которых есть старая цена
    return render(request, 'main/start.html', {'tour': tours})


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

            # Фильтр для горящих туров
            if form.cleaned_data.get('hot_tours'):
                tours = tours.filter(old_price__isnull=False)  # Показываем только туры с old_price

    else:
        form = CustomTourFilterForm()

    return render(request, 'main/tours.html',
                  {'form': form, 'hotel': hotel, 'tour': tours, 'country': country, 'filter': tour_filter})


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

@login_required
def editprofile(request):
    user = request.user  # Получаем текущего пользователя

    if request.method == "POST":
        # Получаем данные из формы
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.date_of_birth = request.POST.get("dob")
        user.phone_number = request.POST.get("phone")
        user.passport_data = request.POST.get("passport")

        user.save()  # Сохраняем изменения в базе данных
        return redirect("profile_page")  # Перенаправление на страницу профиля

    return render(request, "main/editprofile.html")


@login_required
def contracts(request):
    contracts = Contracts.objects.filter(client=request.user)
    return render(request, 'main/contracts.html',  {'contracts': contracts})

@login_required
def process_payment(request):
    if request.method == "POST":
        user = request.user  # Получаем текущего пользователя
        cart = request.session.get("cart", {}).get("tours", [])  # Получаем список ID туров из сессии

        if not cart:
            return redirect("cart_page")  # Если корзина пустая, перенаправляем обратно

        tours = Tour.objects.filter(id__in=cart)  # Получаем объекты туров
        total_price = sum(tour.price for tour in tours)  # Рассчитываем общую стоимость

        # Создаем запись о транзакции (можно добавить проверку успешности платежа)
        transaction = Transaction.objects.create(
            card_number="XXXX-XXXX-XXXX-0000",  # В реальном проекте номер карты не сохраняем!
            amount=total_price,
            status="success"
        )

        # Создаем договор на каждый оплаченный тур
        for tour in tours:
            Contracts.objects.create(
                title=f"Договор на тур {tour.title}",
                client=user,
                tour=tour,
                price=tour.price
            )

        # Очищаем корзину после оплаты
        request.session["cart"] = {"tours": []}
        request.session.modified = True

        return redirect("ordercomplete_page")  # Перенаправляем на страницу подтверждения заказа

    return redirect("cart_page")

