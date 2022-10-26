from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import ReviewRating


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    field_order = ['username', 'email', 'password1', 'password2']

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ReviewForm(ModelForm):

    class Meta:
        model = ReviewRating
        fields = ['health', 'speed', 'body_strength', 'strength_environment', 'talent', 'player']
        choices = ((5, 5), (4, 4), (3, 3), (2, 2), (1, 1))
        widgets = {
            'player': forms.HiddenInput(),
            'health': forms.RadioSelect(choices=choices, attrs={'required': True}),
            'speed': forms.RadioSelect(choices=choices, attrs={'required': True}),
            'body_strength': forms.RadioSelect(choices=choices, attrs={'required': True}),
            'strength_environment': forms.RadioSelect(choices=choices, attrs={'required': True}),
            'talent': forms.RadioSelect(choices=choices, attrs={'required': True})
        }

        labels = {
            'health': 'Здоровье:',
            'speed': 'Скорость:',
            'body_strength': 'Сила:',
            'strength_environment': 'Сила окружения:',
            'talent': 'Талант:'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['player'].required = False
