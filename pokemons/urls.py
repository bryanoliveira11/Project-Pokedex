from django.urls import path
from pokemons import views

app_name = 'pokedex'

urlpatterns = [
    path('', views.index, name='index'),
    path('pokemon/<int:poke_id>/<str:poke_name>/',
         views.pokemon, name='pokemon'),
]
