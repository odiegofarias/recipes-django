from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views


class RecipeCategoryViewTest(RecipeTestBase):
    def test_se_a_view_category_de_recipe_esta_correta(self):
        view = resolve(
            reverse(
                'recipes:category', kwargs={'category_id': 1}
            )
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_retorna_status_code_404_se_nao_encontrou_recipes(self): # noqa: 501
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': 999}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_carrega_recipes(self):
        titulo = 'This is a category test'
        self.make_recipe(title=titulo)

        # executando TEMPLATE
        response = self.client.get(reverse('recipes:category', args=(1,)))
        # Pegando conteúdo da página. OLHAR DEBUG
        content = response.content.decode('utf-8')
        # Verificando toda a receita, retorna todos os valores do BD, OLHAR DEBUG # noqa: 501
        #  response_context_recipes = response.context['recipes']
        # Verificando se os itens abaixos estão contidos no content
        self.assertIn(titulo, content)

    def test_recipe_category_template_nao_carrega_recipes_nao_publicadas(self):
        #  Pegando o CATEGORY.ID da recipe
        recipe = self.make_recipe(is_published=False)

        # executando TEMPLATE
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={
                    'category_id': recipe.category.id,
                },
            )
        )

        self.assertEqual(response.status_code, 404)

    