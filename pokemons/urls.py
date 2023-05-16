from django.urls import path
from pokemons import views

app_name = 'pokedex'

urlpatterns = [
    path('', views.index, name='index'),
    path('pokemon/poke_id=<int:poke_id>/',
         views.pokemon, name='pokemon'),
]
