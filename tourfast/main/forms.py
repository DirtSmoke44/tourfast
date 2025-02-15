from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import AuthenticationForm
from main.models import Buyer
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Buyer
        fields = ("username", "last_name", "email", "password1", "password2")

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'input'}))
    # last_name = forms.CharField(label="Фамилия пользователя", widget=forms.TextInput(attrs={'class': 'input'}))
    # email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class': 'input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'input'}))

