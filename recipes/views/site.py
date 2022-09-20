import os
from recipes.models import Recipe
from django.http import Http404
from utils.pagination import make_pagination
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models import Q
#  from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from tag.models import Tag


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def theory(request, *args, **kwargs):
    #         Model   Manager  Método
    # recipes = Recipe.objects.all()
    # #  Filter retorna uma queryset. O first retorna apenas 1 recipe
    # recipes = recipes.filter(title__icontains='receita').first()

    #  Se não existir, ele levanta uma exceção DoesNotExist
    # try:
    #     recipes = Recipe.objects.get(id=10000)
    # except ObjectDoesNotExist:
    #     recipes = None

    # Recipe.objects.all()

    # #  Pega um específico
    # Recipe.objects.get()

    # # Retorna um objeto do model, não tem como filtrar após isso
    # Recipe.objects.filter().first()
    # Recipe.objects.filter().last()

    #  Operador OR
    """
        recipes = Recipe.objects.filter(
            Q(
                Q(
                    title__icontains='receita',
                    id__gt=2,
                    is_published=True,
                ) |
                Q(
                    title__icontains='pão',
                )
            )
        )[:30]
    """

    #  F sempre para referenciar o campo. Estou tentando pegar uma receita com o mesmo ID do author # noqa: E501
    """
        recipes = Recipe.objects.filter(
            id=F('author__id')
        )[:20]
    """

    #  Pesquisando com valores específicos para ser mais rapido
    """
        recipes = Recipe.objects.values(
            'id', 'author__username', 'title',
        )[:20]
    """

    #  Perigoso. Prestar atenção nos campos que vou usar. Pode ser DEFER
    # recipes = Recipe.objects.only('id', 'title')

    #  Agregadores, Max, MIN, COUNT, MÈDIA
    # recipes = Recipe.objects.values('id', 'title').filter(title__icontains='receita')  # noqa: E501

    # Juntando nome e sobrenome e acrescentando carac com Value  ANNOTATE
    recipes = Recipe.objects.get_published()
    number_of_recipes = recipes.aggregate(number=Count('id'))

    context = {
        'recipes': recipes,
        # Retorna um dicionário. Com isso, preciso pegar o field
        'number_of_recipes': number_of_recipes['number'],
    }

    return render(
        request,
        'recipes/pages/theory.html',
        context=context,
    )


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    #  Alterando as querys no banco de dados e criando os meus filtros
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')

        return qs

    #  Manipulando o contexto. No caso, tenho a paginação e os recipes
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE,
        )
        ctx.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range,
            }
        )

        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False,
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - Category',
        })

        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(  # OU
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            ),
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}"',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True
        })

        return ctx


class RecipeDetailApi(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first()  # noqa: E501

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag |'

        ctx.update({
            'page_title': page_title,
        })

        return ctx
