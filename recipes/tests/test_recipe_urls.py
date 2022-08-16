from django.test import TestCase
from django.urls import reverse


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

    def test_se_a_recipe_search_url_esta_correta(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
