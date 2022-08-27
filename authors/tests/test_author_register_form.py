from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: Diego'),
        ('last_name', 'Ex.: Fernandes'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placholder_esta_correto(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters'),
        ('email', 'The email must be valid.'),
        ('username', ('Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'))  # noqa: E501
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('password', 'Senha'),
        ('password2', 'Repita a senha'),
    ])
    def test_fields_labels(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)
