from django.contrib.auth.forms import UserCreationForm
from .models import Tour, Country, Hotel
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
    hot_tours = forms.BooleanField(required=False, label="Горящие туры")

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Buyer
        fields = ("username", "last_name", "email", "password1", "password2")

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'input'}))
    # last_name = forms.CharField(label="Фамилия пользователя", widget=forms.TextInput(attrs={'class': 'input'}))
    # email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class': 'input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'input'}))

class UserEditForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['username', 'last_name', 'email', 'phone_number', 'date_of_birth', 'passport_data']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class TourEditForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['title', 'country', 'hotel', 'start_date', 'end_date', 'old_price', 'price', 'photo']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(),
        }

    def init(self, args, **kwargs):
        super(TourEditForm, self).init(args, **kwargs)
        self.fields['old_price'].required = False
        self.fields['hotel'].queryset = Hotel.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['hotel'].queryset = Hotel.objects.filter(country_id=country_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.country:
            self.fields['hotel'].queryset = self.instance.country.hotels.all()

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['title', 'country', 'hotel', 'start_date', 'end_date', 'old_price', 'price', 'photo']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(),
        }


def __init__(self, *args, **kwargs):
    super(TourForm, self).__init__(*args, **kwargs)
    self.fields['old_price'].required = False
    self.fields['hotel'].queryset = Hotel.objects.none()  # пусто при загрузке

    if 'country' in self.data:
        try:
            country_id = int(self.data.get('country'))
            self.fields['hotel'].queryset = Hotel.objects.filter(country_id=country_id)
        except (ValueError, TypeError):
            pass
    elif self.instance.pk:
        self.fields['hotel'].queryset = self.instance.country.hotels.all()
