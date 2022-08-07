from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views


class RecipeURLsTest(TestCase):
    def test_se_a_home_url_de_recipe_esta_correta(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_se_a_category_url_de_recipe_esta_correta(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_se_a_recipe_detalhe_url_de_recipe_esta_correta(self):
        url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(url, '/recipes/1/')


class RecipeViewsTest(TestCase):
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
