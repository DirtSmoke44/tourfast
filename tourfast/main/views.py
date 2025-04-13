from django.http import HttpResponse

from main.models import Hotel, Country, Tour, Contracts, Buyer, Transaction, Booking
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
from django.contrib import messages
from datetime import datetime
from decimal import Decimal

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
    # Туры в корзине
    cart = request.session.get('cart', {'tours': []})
    tour_ids = cart.get('tours', [])
    tours = Tour.objects.filter(id__in=tour_ids)

    # Бронирования в корзине
    booking_ids = request.session.get('bookings', [])
    bookings = Booking.objects.filter(id__in=booking_ids, client=request.user)

    # Расчет общей стоимости
    tours_total = sum(tour.price for tour in tours)
    bookings_total = sum(booking.price for booking in bookings)
    total_price = tours_total + bookings_total

    return render(request, 'main/cart.html', {
        'tours': tours,
        'bookings': bookings,
        'tours_total': tours_total,
        'bookings_total': bookings_total,
        'total_price': total_price,
    })

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
def cancel_booking(request, booking_id):
    if request.method == 'POST':
        try:
            booking = Booking.objects.get(id=booking_id, client=request.user)

            # Удаляем из сессии
            if 'bookings' in request.session and booking.id in request.session['bookings']:
                request.session['bookings'].remove(booking.id)
                request.session.modified = True

            booking.delete()
            messages.success(request, 'Бронирование отменено')
        except Exception as e:
            messages.error(request, f'Ошибка при отмене бронирования: {str(e)}')

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
    """Очищает корзину (и туры, и бронирования)."""
    # Очищаем туры
    request.session['cart'] = {'tours': []}

    # Очищаем бронирования
    if 'bookings' in request.session:
        # Получаем ID бронирований перед их удалением
        booking_ids = request.session['bookings']
        # Удаляем сами бронирования из базы данных
        Booking.objects.filter(id__in=booking_ids, client=request.user).delete()
        # Очищаем сессию
        request.session['bookings'] = []

    request.session.modified = True
    messages.success(request, 'Корзина полностью очищена')
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

def map(request):
    return render(request, 'main/map.html')

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


@login_required
def create_booking(request):
    if request.method == 'POST':
        try:
            tour_id = request.POST.get('tour_id')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            guests = int(request.POST.get('guests', 1))

            # Получаем тур
            tour = Tour.objects.get(id=tour_id)
            price = (tour.price / 100) * 30
            # Создаем бронирование
            booking = Booking.objects.create(
                client=request.user,
                tour=tour,
                check_in=start_date,
                check_out=end_date,
                guests=guests,
                price=price,
                status='pending'
            )

            # Добавляем в корзину (сессию)
            if 'bookings' not in request.session:
                request.session['bookings'] = []

            if booking.id not in request.session['bookings']:
                request.session['bookings'].append(booking.id)
                request.session.modified = True

            messages.success(request, 'Тур успешно забронирован и добавлен в корзину!')
            return redirect('cart_page')

        except Exception as e:
            messages.error(request, f'Ошибка при бронировании: {str(e)}')
            return redirect('tours_page')

    return redirect('tours_page')




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
        user = request.user

        # Получаем данные из сессии
        tour_ids = request.session.get("cart", {}).get("tours", [])
        booking_ids = request.session.get("bookings", [])

        if not tour_ids and not booking_ids:
            return redirect("cart_page")  # Если корзина пустая

        # Получаем объекты из БД
        tours = Tour.objects.filter(id__in=tour_ids)
        bookings = Booking.objects.filter(id__in=booking_ids, client=user)

        # Рассчитываем общую стоимость
        total_amount = sum(tour.price for tour in tours) + sum(booking.price for booking in bookings)

        # Создаем транзакцию
        transaction = Transaction.objects.create(
            card_number="XXXX-XXXX-XXXX-0000",
            amount=total_amount,
            status="success"
        )

        # Создаем договоры для бронирований (без связи через ForeignKey)
        for booking in bookings:
            Contracts.objects.create(
                title=f"Договор бронирования #{booking.id}",
                client=user,
                tour=booking.tour,  # Связь через тур
                price=booking.price,
                date=booking.booking_date

            )
            # Обновляем статус бронирования через прямое присвоение
            Booking.objects.filter(id=booking.id).update(status='paid')

        # Создаем договоры для туров
        for tour in tours:
            Contracts.objects.create(
                title=f"Договор тура #{tour.id}",
                client=user,
                tour=tour,
                price=tour.price,

            )

        # Очищаем корзину
        request.session["cart"] = {"tours": []}
        request.session["bookings"] = []
        request.session.modified = True

        return redirect("ordercomplete_page")

    return redirect("cart_page")

def download_contract(request, contract_id):
    contract = get_object_or_404(Contracts, id=contract_id)

    # Формируем текст для договора
    contract_text = f"""
    Договор №{contract.id}
    ----------------------
    Тур: {contract.tour.title}
    Дата оформления: {contract.date.strftime("%d.%m.%Y %H:%M")}

    Клиент:
    Имя: {contract.client.username}
    Фамилия: {contract.client.last_name}

    Детали тура:
    Страна: {contract.tour.country}
    Отель: {contract.tour.hotel}
    Даты: {contract.tour.start_date.strftime("%d.%m.%Y")} - {contract.tour.end_date.strftime("%d.%m.%Y")}
    Стоимость за ночь: {contract.tour.hotel.price_per_night:.2f} Рублей
    Общая стоимость: {contract.price:.2f} Рублей

    Статус оплаты: Подтверждён
    """

    # Создаём HTTP-ответ с файлом .txt
    response = HttpResponse(contract_text, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=contract_{contract.id}.txt'
    return response
