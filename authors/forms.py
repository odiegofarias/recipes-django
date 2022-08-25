from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        # labels = {
        #     'first_name': 'Primeiro nome',
        #     'last_name': 'Último nome',
        #     'username': 'Usuário',
        #     'email': 'E-mail',
        #     'password': 'Senha',
        # }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Digite seu usuário'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite seu password'
            })
        }