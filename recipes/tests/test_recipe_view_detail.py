from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views


class RecipeDetailViewTest(RecipeTestBase):
    def test_se_a_view_recipe_detalhes_de_recipe_esta_correta(self):
        view = resolve(
            reverse(
                'recipes:recipe', kwargs={'id': 1}
            )
        )
        self.assertIs(view.func, views.recipe)

    

    def test_recipe_recipe_detalhe_view_retorna_status_code_404_se_nao_encontrou_recipe(self): # noqa: 501
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': 999}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detalhes_template_carrega_recipe_correta(self):
        titulo = 'This is a detail page - Carrega uma receita'
        self.make_recipe(title=titulo)

        # executando TEMPLATE
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': 1
                },
            )
        )
        # Pegando conteúdo da página. OLHAR DEBUG
        content = response.content.decode('utf-8')
        # Verificando toda a receita, retorna todos os valores do BD, OLHAR DEBUG # noqa: 501
        #  response_context_recipes = response.context['recipes']
        # Verificando se os itens abaixos estão contidos no content
        self.assertIn(titulo, content)

    def test_recipe_detalhes_template_nao_carrega_recipe_nao_publicada(self):
        #  Pegando o CATEGORY.ID da recipe
        recipe = self.make_recipe(is_published=False)

        # executando TEMPLATE
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': recipe.id,
                },
            )
        )

        self.assertEqual(response.status_code, 404)