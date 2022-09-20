from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from tag.models import Tag
from ..serializers import TagSerializer
#  from rest_framework import status


@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]
    #  Sempre que mandar uma queryset, precisa colocar "many=True"
    serializer = RecipeSerializer(
        instance=recipes,
        many=True,
        context={'request': request}
    )

    return Response(serializer.data)


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk,
    )
    serializer = RecipeSerializer(
        instance=recipe,
        many=False,
        context={'request': request}
    )
    #  Sempre que mandar uma queryset, precisa colocar "many=True"
    # serializer = RecipeSerializer(instance=recipe, many=False)

    return Response(serializer.data)


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
