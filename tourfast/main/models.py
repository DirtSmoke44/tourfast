from django.db import models
from django.contrib.auth.models import User, AbstractUser, Permission, Group
from django.conf import settings
import os

class Clients(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.user}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Buyer(AbstractUser): # Клиенты

    last_name = models.CharField('Фамилия', max_length=50, null=True)
    email = models.EmailField('Email', max_length=50)
    # password1 = models.CharField('Пароль', max_length=50)
    # password2 = models.CharField('Пароль', max_length=50)
    groups = models.ManyToManyField(Group, related_name='buyers')
    user_permissions = models.ManyToManyField(Permission, related_name='buyers')
    phone_number = models.CharField('Номер телефона', max_length=11, null=True)
    # address = models.TextField('Адрес', null=True)
    date_of_birth = models.DateField('Дата рождения', null=True)
    passport_data = models.CharField('Паспортные данные', max_length=50, null=True)  # Новое поле
    photo = models.ImageField('Фото профиля', upload_to='main/profilephotos/', null=True, blank=True)
    is_special = models.BooleanField(default=False, verbose_name='Особый пользователь')




class Country(models.Model): # Страны
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000, unique=True, null=True)
    photo = models.ImageField('Фото страны', upload_to='main/countryphotos/', null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

class Hotel(models.Model): # Отели
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="hotels")
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    stars = models.PositiveSmallIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField('Фото отеля', upload_to='main/hotelphotos/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country.name})"

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'

class Tour(models.Model): # Туры
    title = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="tours")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="tours")
    start_date = models.DateField()
    end_date = models.DateField()
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # типа для скидки
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField('Фото тура', upload_to='main/tourphotos/', null=True, blank=True)

    def delete(self, *args, **kwargs):
        # удаление файла с диска, если он существует
        if self.photo and os.path.isfile(self.photo.path):
            os.remove(self.photo.path)
        super().delete(*args, **kwargs)

    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return round((self.old_price - self.price) / self.old_price * 100, 2)
        return 0

    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"

    def is_available_for_dates(self, start_date, end_date):
        """Проверяет, доступен ли тур для указанных дат"""
        overlapping_bookings = self.bookings.filter(
            models.Q(check_in__lte=end_date) &
            models.Q(check_out__gte=start_date) &
            ~models.Q(status='cancelled'))
        return not overlapping_bookings.exists()

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class Transaction(models.Model):  # Транзакции

    card_number = models.CharField(max_length=16)
    amount = models.DecimalField(max_digits=100000, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


class Contracts(models.Model):

    title = models.CharField(max_length=200)
    client = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="contracts")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="contracts")
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="transaction", null=True)

    def str(self):
        return self.title

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договора'



class Booking(models.Model):
    client = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="bookings")
    tour = models.ForeignKey(Tour, on_delete=models.PROTECT, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in = models.DateField(null=True)  # Дата заезда
    check_out = models.DateField(null=True)  # Дата выезда
    guests = models.PositiveIntegerField(default=1, null=True)  # Количество гостей
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)

    STATUS_CHOICES = [
        ('pending', 'Ожидание подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('paid', 'Оплачено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено')
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Дополнительные услуги (можно хранить как JSON или текстовое поле)
    extras = models.JSONField(null=True, blank=True)

    # Ссылка на договор (если требуется)
    contract = models.OneToOneField(
        Contracts,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='booking'
    )

    class Meta:
        ordering = ['-booking_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['check_in', 'check_out']),
        ]
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f"Бронирование #{self.id} - {self.tour.title} ({self.client.username})"

    def save(self, *args, **kwargs):
        # Автоматическое установление цены при создании
        if not self.pk and not self.price:
            self.price = self.tour.price
        super().save(*args, **kwargs)

    @property
    def hotel(self):

        return self.tour.hotel

    @property
    def country(self):

        return self.tour.country

    @property
    def duration(self):

        return (self.check_out - self.check_in).days

    def get_total_price(self):

        return self.price * self.guests * self.duration

