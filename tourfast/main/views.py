import os

from django.http import HttpResponse
from .forms import TourForm, TourEditForm
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
from django.http import JsonResponse

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

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
def edittour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        form = TourEditForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tours_page')
    else:
        form = TourEditForm(instance=tour)

    return render(request, "main/edittour.html", {'tour': tour, 'form': form})

@login_required
def contracts(request):
    query = request.GET.get('search', '')

    if request.user.is_special:
        contracts = Contracts.objects.all()
        if query:
            contracts = contracts.filter(client__last_name__icontains=query)
    else:
        contracts = Contracts.objects.filter(client=request.user)

    return render(request, 'main/contracts.html', {
        'contracts': contracts,
        'search_query': query,
    })

def load_hotels(request):
    country_id = request.GET.get('country_id')
    hotels = Hotel.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(hotels), safe=False)

@login_required
def process_payment(request):
    if request.method == "POST":
        user = request.user

        # Получаем данные из сессии
        tour_ids = request.session.get("cart", {}).get("tours", [])
        booking_ids = request.session.get("bookings", [])
        card_number = request.POST.get('card_number')
        if not tour_ids and not booking_ids:
            return redirect("cart_page")  # Если корзина пустая

        # Получаем объекты из БД
        tours = Tour.objects.filter(id__in=tour_ids)
        bookings = Booking.objects.filter(id__in=booking_ids, client=user)

        # Рассчитываем общую стоимость
        total_amount = sum(tour.price for tour in tours) + sum(booking.price for booking in bookings)

        # Создаем транзакцию
        transaction = Transaction.objects.create(
            card_number=card_number,
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
                date=booking.booking_date,
                transaction=transaction

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
                transaction=transaction
            )

        # Очищаем корзину
        request.session["cart"] = {"tours": []}
        request.session["bookings"] = []
        request.session.modified = True

        return redirect("ordercomplete_page")

    return redirect("cart_page")

def generate_contract_pdf(contract):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Путь к шрифту Arial
    font_path = os.path.join('main', 'static', 'main', 'fonts', 'arial.ttf')
    pdfmetrics.registerFont(TTFont('Arial', font_path))
    p.setFont('Arial', 11)

    text_object = p.beginText(2 * cm, height - 2 * cm)
    text_object.setFont("Arial", 11)

    lines = [
        f"Ваучер №{contract.id} НА ТУРИСТИЧЕСКОЕ ОБСЛУЖИВАНИЕ",
        "Туристическая фирма: tourFAST",
        "Адрес: Россия, Казань, Ул. Проспекта Победы, д.68",
        "Телефон: +7 (843) 737-33-67",
        "Email: tourfastsupport@gmail.com",
        "ОГРН: 1234567890123    ИНН: 9876543210",
        "",
        f"Клиент: {contract.client.last_name} {contract.client.username}",
        f"Email клиента: {contract.client.email}",
        f"Паспортные данные: {getattr(contract.client, 'passport_data', 'Не указано')}",
        "",
        f"Название тура: {contract.tour.title}",
        f"Страна: {contract.tour.country}",
        f"Отель: {contract.tour.hotel.name}",
        f"Адрес отеля: {contract.tour.hotel.address}, {contract.tour.hotel.city}",
        f"Даты поездки: с {contract.tour.start_date.strftime('%d.%m.%Y')} по {contract.tour.end_date.strftime('%d.%m.%Y')}",
        f"Цена за ночь: {contract.tour.hotel.price_per_night:.2f} руб.",
        f"Общая стоимость тура: {contract.price:.2f} руб.",
        "",
        f"Номер карты: {contract.transaction.card_number if contract.transaction else 'Не указано'}",
        "Статус оплаты: Подтверждён",
        "",
        "Прочие условия:",
        "- Турфирма обязуется предоставить полный комплекс туристических услуг.",
        "- Клиент обязуется соблюдать правила проживания и законы страны пребывания.",
        "- При отказе от тура применяются штрафные санкции.",
        "",
        f"Дата заключения договора: {contract.date.strftime('%d.%m.%Y')}",
        "",
        "Подписи сторон:",
        "Турфирма tourFAST: _____________",
        "Клиент: _____________",
        "",
        "Спасибо, что выбрали tourFAST! Желаем вам приятного отдыха!"
    ]

    for line in lines:
        text_object.textLine(line)

    p.drawText(text_object)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def download_contract(request, contract_id):
    contract = get_object_or_404(Contracts, id=contract_id)
    pdf_buffer = generate_contract_pdf(contract)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=contract_{contract.id}.pdf'
    return response

@login_required
def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        user = request.user
        user.photo = request.FILES['photo']
        user.save()
        messages.success(request, 'Аватар успешно обновлен!')
    return redirect('profile_page')


@login_required
def create_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('tours_page')  # или другая страница после создания
    else:
        form = TourForm()
    return render(request, 'main/create_tour.html', {'form': form})

def load_hotels(request):
    country_id = request.GET.get('country_id')
    hotels = Hotel.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(hotels), safe=False)

@login_required
def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    tour.delete()
    return redirect('tours_page')  # или другая страница после удаления