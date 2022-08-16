from django.core.exceptions import ValidationError
from .test_recipe_base import RecipeTestBase, Recipe

from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        ...

        return super().setUp()
        """
        Todos os testes que forem gerar erros, precisa ser feito
        uma validação com assertRaises ValidationError
        """
    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='Teste default Category'),
            author=self.make_author(username='Diego'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug-for-no-defaults',
            preparation_time_unit='Minutos',
            preparation_time=10,
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe preparation steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_campos_max_length(self, field, max_length):
        #  SetAttr pega o atributo dinamicamente
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # Validação

    #  Testando DEFAULTS no models que mudam a lógica do meu template
    def test_recipe_prepatarion_steps_is_html_e_falso_por_padrao(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe prepatarion_steps_is_html não é falso',
        )

    def test_recipe_is_published_eh_falso_por_padrao(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published não é falso',
        )

    def test_recipe_representacao_de_string(self):
        needed = 'Testing Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe),
            needed,
            msg=f'A representação da string precisa ser igual ao needed: {needed}'  # noqa: 501

        )
    
    
