from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from authors.validators import AuthorRecipeValidator

from collections import defaultdict


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = (
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
        )
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'preparation_time': 'Tempo de preparo',
            'preparation_time_unit': 'Unidade de tempo de preparo',
            'servings': 'Porções',
            'servings_unit': 'Unidade de porções',
            'preparation_steps': 'Modo de preparo',
            'cover': 'Imagem de Capa',
        }

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2',
                }
            ),
            #  Trocando o campo servings_unit para select no input do html
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorRecipeValidator(self.cleaned_data)

        return super_clean

   