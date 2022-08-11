from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views


class RecipeViewsTest(RecipeTestBase):
    def test_se_a_view_home_de_recipe_esta_correta(self):
        #  resolve: qual função está sendo usada por uma URL
        '''
            '==' checa se um valor é igual ao outro
            'is' checa se a referência de memória(endereço da memória) é igual
                lista_1 = []
                lista_2 = lista_1

        '''
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_se_a_view_category_de_recipe_esta_correta(self):
        view = resolve(
            reverse(
                'recipes:category', kwargs={'category_id': 1}
            )
        )
        self.assertIs(view.func, views.category)

    def test_se_a_view_recipe_detalhes_de_recipe_esta_correta(self):
        view = resolve(
            reverse(
                'recipes:recipe', kwargs={'id': 1}
            )
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_home_view_retorna_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_retorna_status_code_404_se_nao_encontrou_recipes(self): # noqa: 501
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': 999}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_recipe_detalhe_view_retorna_status_code_404_se_nao_encontrou_recipe(self): # noqa: 501
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': 999}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_view_carrega_template_correto(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # Pode SKIPAR um TEST com @SKIP('WPI')
    def test_recipe_home_template_mostra_no_recipe_founds_se_nao_tem_receita(self): # noqa: 501      
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Nenhuma receita para mostrar',
            response.content.decode('utf-8'),
        )

    def test_recipe_home_template_carrega_recipes(self):
        self.make_recipe(category_data={
            'name': 'Café da manhã'
        })

        # executando TEMPLATE
        response = self.client.get(reverse('recipes:home'))
        # Pegando conteúdo da página. OLHAR DEBUG
        content = response.content.decode('utf-8')
        # Verificando toda a receita, retorna todos os valores do BD, OLHAR DEBUG # noqa: 501
        response_context_recipes = response.context['recipes']
        # Verificando se os itens abaixos estão contidos no content
        self.assertIn('Recipe Title', content)
        self.assertIn('Café da manhã', content)
        self.assertEqual(len(response_context_recipes), 1)

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

    def test_recipe_home_template_nao_carrega_recipes_nao_publicadas(self):
        self.make_recipe(is_published=False)

        # executando TEMPLATE
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'Nenhuma receita para mostrar',
            response.content.decode('utf-8'),
        )

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

