from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django import forms
from django.contrib.auth.models import User
from .models import *


class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput,
        max_length=30, min_length=5, required=True, label='Login'
    )
    first_name = forms.CharField(
        widget=forms.TextInput,
        max_length=30, required=True, label='Firstname'
    )
    last_name = forms.CharField(
        widget=forms.TextInput,
        max_length=30, required=True, label='Lastname'
    )
    email = forms.EmailField(
        widget=forms.TextInput,
        required=True, max_length=254, label='E-mail'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput, min_length=8, label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, min_length=8, label='Repeat password'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError('Such user already exists')
        except User.DoesNotExist:
            return username

    def save(self):
        data = self.cleaned_data
        password = data.get('password1')
        u = User()

        u.username = data.get('username')
        u.password = make_password(password)
        u.email = data.get('email')
        u.first_name = data.get('first_name')
        u.last_name = data.get('last_name')
        u.is_active = True
        u.is_superuser = False
        u.save()

        return authenticate(username=u.username, password=password)


class AuthForm(forms.Form):
    login = forms.CharField(
        widget=forms.TextInput,
        max_length=30,
        label='Login'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Passsword'
    )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login', ''), password=data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError('The user is not active')
        else:
            raise forms.ValidationError('Wrong username or password')


class AddBookForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={'placeholder': 'Name', 'id': 'new_name'}
        )
    )

    author = forms.CharField(
        widget=forms.widgets.TextInput(
            attrs={'placeholder': 'Author', 'id': 'new_author'}
        )
    )

    description = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={'placeholder': 'description', 'id': 'new_description'}
        ),
    )

    image = forms.ImageField(
        required=False,
        widget=forms.widgets.ClearableFileInput(
            attrs={
                'accept': 'image/jpeg, image/png, image/gif',
                'id': 'new_image',
                'class': 'ask-signup-avatar-input'
            }
        )
    )

    def fill_object(self):
        return Book.objects.create(
            name=self.cleaned_data['name'],
            author=self.cleaned_data['author'],
            description=self.cleaned_data['description'],
            image=self.cleaned_data['image']
        )
