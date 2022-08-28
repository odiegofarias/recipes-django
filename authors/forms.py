from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters',
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: Diego')
        add_placeholder(self.fields['last_name'], 'Ex.: Fernandes')
        add_placeholder(self.fields['password'], 'Your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='Primeiro nome'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Último nome'
    )

    username = forms.CharField(
        error_messages={
            'required': 'This field must not be empty.',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must be a maximum of 50 characters'
        },
        help_text=(
            'Username must have letters, numbers or one of those @/./+/-/_ '
            'The length should be between 4 and 50 characters'
        ),
        label='Usuário',
        min_length=4, max_length=50,
    )

    email = forms.EmailField(
        error_messages={'required': 'E-mail is required.'},
        help_text='The email must be valid.',
        label='E-mail',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={'required': 'Password must not be empty.'},
        label='Senha',
        validators=[strong_password],
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters'
        ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repita a senha',
        error_messages={'required': 'Please, repeat your password.'},
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is alreadt in use',
                code='invalid',
            )

        return email

    # Verificando se um campo é igual ao outro
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'As senhas são diferentes',
                code='invalid'
            )
            # Colocando o erro no field "Password"
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                    # Posso colocar uma lista de erros, como:
                    # Letras maiúsculas e minusculas e etc
                ]
            })

    # #  Validação de campo "CLEAN_FIELD"
    # def clean_password(self):
    #     data = self.cleaned_data.get('password')

    #     if 'atenção' in data:
    #         raise ValidationError(
    #             'Não digite %(value)s no campo password',
    #             code='invalid',
    #             params={'value': '"atenção"'}
    #         )

    #     return data

    #     #  Validação de campo
    # def clean_first_name(self):
    #     data = self.cleaned_data.get('first_name')

    #     if 'Jhon Wick' in data:
    #         raise ValidationError(
    #             'Não digite %(value)s no campo first_name',
    #             code='invalid',
    #             params={'value': '"Jhon Wick"'}
    #         )

    #     return data
