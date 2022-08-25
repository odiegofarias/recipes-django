from django.urls import path
from . import views

# recipes:recipe
app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='create'),
]
