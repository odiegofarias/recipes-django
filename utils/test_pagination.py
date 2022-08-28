from unittest import TestCase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_cria_um_range_de_paginacao_e_retorna_range_de_paginacao(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

    def test_verifica_se_os_ranges_do_meio_estao_correstos(self):
        #  Current page = 10 - Qtd Pages = 2 - Middle Page = 2
        #  Aqui MUDA! 
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=4,
            current_page=10,
        )['pagination']

        self.assertEqual([9, 10, 11, 12], pagination)

        #  Current page = 12 - Qtd Pages = 2 - Middle Page = 2
        #  Aqui MUDA!
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=4,
            current_page=12,
        )['pagination']

        self.assertEqual([11, 12, 13, 14], pagination)

    def test_primeiro_numero_do_range_eh_estatico_e_o_restante_esta_no_meio(self):  # noqa: E501
        #  Current page = 1 - Qtd Pages = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

        #  Current page = 2 - Qtd Pages = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

        #  Current page = 3 - Qtd Pages = 2 - Middle Page = 2
        #  Aqui MUDA!
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=4,
            current_page=3,
        )['pagination']

        self.assertEqual([2, 3, 4, 5], pagination)

        #  Current page = 4 - Qtd Pages = 2 - Middle Page = 2
        #  Aqui MUDA!
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=4,
            current_page=4,
        )['pagination']

        self.assertEqual([3, 4, 5, 6], pagination)

    def test_criando_paginacao_range_estatica_quando_proxima_page_eh_ultima(self):  # noqa: E501
        #  Current page = 19 - Qtd Pages = 2 - Middle Page = 2
        #  Aqui MUDA!
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=4,
            current_page=20,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

        #  Current page = 20 - Qtd Pages = 2 - Middle Page = 2
        #  Aqui MUDA!
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=4,
            current_page=20,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

        #  Current page = 21 - Qtd Pages = 2 - Middle Page = 2
        #  Aqui MUDA!
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=4,
            current_page=21,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)