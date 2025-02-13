from django.db import models
from django.contrib.auth.models import User, AbstractUser, Permission, Group


class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField('Имя', max_length=50, null=True)
    last_name = models.CharField('Фамилия', max_length=50, null=True)
    phone_number = models.CharField('Номер телефона', max_length=11, null=True)
    address = models.TextField('Адрес', null=True)
    date_of_birth = models.DateField('Дата рождения', null=True)
    passport_data = models.CharField('Паспортные данные', max_length=50, null=True)  # Новое поле

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Buyer(AbstractUser):
    first_name = models.CharField('Имя', max_length=50, null=True)
    last_name = models.CharField('Фамилия', max_length=50, null=True)
    phone_number = models.CharField('Номер телефона', max_length=11, null=True)
    address = models.TextField('Адрес', null=True)
    date_of_birth = models.DateField('Дата рождения', null=True)
    passport_data = models.CharField('Паспортные данные', max_length=50, null=True)  # Новое поле
    email = models.EmailField('Email', max_length=50)
    password1 = models.CharField('Пароль', max_length=50)
    password2 = models.CharField('Пароль', max_length=50)
    groups = models.ManyToManyField(Group, related_name='buyers')
    user_permissions = models.ManyToManyField(Permission, related_name='buyers')

class Transaction(models.Model):
    card_number = models.CharField(max_length=16)
    amount = models.DecimalField(max_digits=100000, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")  # например, "успешно" или "ошибка"
    created_at = models.DateTimeField(auto_now_add=True)

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

class Hotel(models.Model):
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

class Tour(models.Model):
    title = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="tours")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="tours")
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField('Фото тура', upload_to='main/tourphotos/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

class Booking(models.Model):
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

class Review(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="reviews")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.client.user.username} на {self.hotel.name}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
