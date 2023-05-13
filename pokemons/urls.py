from django.urls import path
from pokemons import views

app_name = 'pokedex'

urlpatterns = [
    path('', views.index, name='index'),
]
