from django.shortcuts import render
from .index_view import get_pokemon_data
import requests


def pokemon(request, poke_id, poke_name):

    context = {
        'poke_id': poke_id,
        'poke_name': poke_name
    }

    print(poke_id)

    return render(request, 'pokedex/pokemon.html', context)
