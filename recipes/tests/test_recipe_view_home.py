from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views
from unittest.mock import patch


class RecipeHomeViewTest(RecipeTestBase):
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

    def test_recipe_home_view_retorna_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

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

    def test_recipe_home_template_nao_carrega_recipes_nao_publicadas(self):
        self.make_recipe(is_published=False)

        # executando TEMPLATE
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'Nenhuma receita para mostrar',
            response.content.decode('utf-8'),
        )

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_eh_paginado(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        # with patch('recipes.views.PER_PAGE', new=3): Também pode ser assim
        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        #  Pegando o número de páginas
        self.assertEqual(paginator.num_pages, 3)
        #  Acessando cada página e verificando o números de recipes
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)

    def test_page_query_invalida_usa_page_um(self):
        """
            Criando 8 receitas e com o gerenciador de contexto,
            colocando 3 receitas por página
            caso, teremos 3 páginas ao todo.
        """
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=1A')

            # Chamando um valor inválido(1A), ele deve mandar para página 1
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            #  Mandando um valor correto, ele manda para a página específica
            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                2
            )
