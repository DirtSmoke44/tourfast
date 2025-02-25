from django.db import models
from django.contrib.auth.models import User, AbstractUser, Permission, Group
from django.conf import settings

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

class Transaction(models.Model): # Транзакции
    card_number = models.CharField(max_length=16)
    amount = models.DecimalField(max_digits=100000, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")  # например, "успешно" или "ошибка"
    created_at = models.DateTimeField(auto_now_add=True)

class Country(models.Model): # Страны
    name = models.CharField(max_length=100, unique=True)
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

    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return round((self.old_price - self.price) / self.old_price * 100, 2)
        return 0

    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

class Booking(models.Model): # Бронирование
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="bookings")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Ожидание"), ("confirmed", "Подтверждено"), ("cancelled", "Отменено")],
        default="pending"
    )

    def __str__(self):
        return f"Бронирование {self.client.user.username} - {self.tour.title}"

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

class Contracts(models.Model):

    title = models.CharField(max_length=200)
    client = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="contracts")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="contracts")
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def str(self):
        return self.title

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договора'
