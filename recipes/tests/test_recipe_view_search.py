from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views


class RecipeSearchViewTest(RecipeTestBase):
    def test_se_a_funcao_view_search_de_recipe_esta_correta(self):
        view = resolve(reverse('recipes:search'))

        self.assertIs(view.func.view_class, views.RecipeListViewSearch)

    def test_se_a_search_recipe_carrega_o_template_correto(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')

        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_retorna_404_se_nao_encontrar_termo(self):
        url = reverse('recipes:search')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    #  Checando o valor escapado SCRIPTS JS
    def test_recipe_search_term_esta_no_title_da_page_e_escapado(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8'),
        )

    def test_recipe_search_pode_encontrar_recipe_por_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one',
            title=title1,
            author_data={'username': 'one'},
        )

        recipe2 = self.make_recipe(
            slug='two',
            title=title2,
            author_data={'username': 'two'},
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_pode_encontrar_recipe_por_descricao(self):
        description1 = 'This is description one'
        description2 = 'This is description two'

        recipe1 = self.make_recipe(
            slug='one',
            description=description1,
            author_data={'username': 'one'},
        )
        recipe2 = self.make_recipe(
            slug='two',
            description=description2,
            author_data={'username': 'two'},
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={description1}')
        response2 = self.client.get(f'{search_url}?q={description2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

