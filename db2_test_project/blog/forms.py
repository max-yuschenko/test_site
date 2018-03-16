from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django.forms.widgets import DateInput


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = MyUser
        fields = ('email', 'date_of_birth', 'country', 'city', 'password1', 'password2')
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }
