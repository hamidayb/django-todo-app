from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django import forms
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Please add a valid email address')

    class Meta:
        model = User
        fields = ['email', 'name', 'city', 'age', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.users.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} already in use.')

