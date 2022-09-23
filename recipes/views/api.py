from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from tag.models import Tag
from ..serializers import TagSerializer
from rest_framework import status
from rest_framework.views import APIView


class RecipeAPIv2List(APIView):
    def get(self, request):
        recipes = Recipe.objects.get_published()[:10]
        #  Sempre que mandar uma queryset, precisa colocar "many=True"
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author_id=1, category_id=1,
            tags=[1, 2],
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class RecipeApiv2Detail(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(
            Recipe.objects.get_published(),
            pk=pk,
        )

        return recipe

    def get(self, request, pk):
        recipe = self.get_recipe(pk=pk)
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        recipe = self.get_recipe(pk=pk)
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data
        )

    def delete(self, request, pk):
        recipe = self.get_recipe(pk=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
