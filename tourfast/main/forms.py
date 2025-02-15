from django.contrib.auth.forms import UserCreationForm
from .models import Tour, Country
from django.contrib.auth.forms import AuthenticationForm
from main.models import Buyer
from django import forms
from .filters import TourFilter

class CustomTourFilterForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, label="Страна")
    price_min = forms.DecimalField(required=False, min_value=0, label="Цена от")
    price_max = forms.DecimalField(required=False, min_value=0, label="Цена до")
    duration_min = forms.IntegerField(required=False, min_value=0, label="Мин. длительность")
    duration_max = forms.IntegerField(required=False, min_value=0, label="Макс. длительность")

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Buyer
        fields = ("username", "last_name", "email", "password1", "password2")

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'input'}))
    # last_name = forms.CharField(label="Фамилия пользователя", widget=forms.TextInput(attrs={'class': 'input'}))
    # email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class': 'input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'input'}))

