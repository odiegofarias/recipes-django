from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
import uuid


class Category(models.Model):
    name = models.CharField(max_length=65)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True, default=uuid.uuid1)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default=''
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        blank=True, default=None,
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            super(Recipe, self).save()
            self.slug = '%s-%i' % (slugify(self.title), self.id)

        super(Recipe, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
