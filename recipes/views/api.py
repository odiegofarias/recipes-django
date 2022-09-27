from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer
from django.shortcuts import get_object_or_404
from tag.models import Tag

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 10


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

    def get_queryset(self):
        qs = super().get_queryset()

        """
            Pega os parametros enviados na url
            Nas query strings, to pegando o category_id
            Retorna todas as receita que estão nessa categoria
                print('Parametros', self.kwargs)
                print('Query Strings', self.request.query_params)
        """

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk,
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        # context={'request': request}
    )

    return Response(serializer.data)
