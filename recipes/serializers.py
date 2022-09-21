from rest_framework import serializers
# from django.contrib.auth.models import User
from tag.models import Tag
from .models import Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'author_name',
            'title',
            'description',
            'category',
            'public',
            'preparation',
            'tags',
            'tags_names',
            'tag_links',
        ]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True,
    )
    preparation = serializers.SerializerMethodField(
        read_only=True,
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )
    author_name = serializers.StringRelatedField(
        source='author'
    )

    tags_names = TagSerializer(
        many=True,
        source='tags',
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        # queryset=Tag.objects.all(),
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    # Utilizado quando precisamos validar um campo específico
    def validate_title(self, value):
        title = value

        if len(title) < 5:
            raise serializers.ValidationError('O título precisa ter mais de 5 caracteres')  # noqa: E501

        return title

    # Utilizado quando precisamos do valor de mais um campo
    def validate(self, attrs):
        super_validate = super().validate(attrs)

        title = attrs.get('title')
        description = attrs.get('description')

        if title == description:
            raise serializers.ValidationError(
                {
                    "title": ["Posso", "Ter", "Mais de um erro"],
                    "description": ["Posso", "Ter", "Mais de um erro"]
                }
            )

        return super_validate
