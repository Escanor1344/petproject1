from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import ReviewRating


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password repeat', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Mail', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    field_order = ['username', 'email', 'password1', 'password2']

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


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
            'health': 'Health:',
            'speed': 'Speed:',
            'body_strength': 'Body strength:',
            'strength_environment': 'Environment:',
            'talent': 'Talent:'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['player'].required = False
