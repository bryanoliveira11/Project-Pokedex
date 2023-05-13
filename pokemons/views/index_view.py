from django.shortcuts import render
from django.core.paginator import Paginator
import requests


def index(request):
    response_base = requests.get("https://pokeapi.co/api/v2/pokemon/")
    pokemons = []

    for poke_id in range(0, 20):
        # getting pokemon data
        response_pokemon = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{poke_id + 1}/"
        )

        pokemon_data = {
            'id': poke_id,
            'name': response_base.json()['results'][poke_id]['name'],
            'image_default':
                response_pokemon.json()['sprites']['front_default'],
        }
        pokemons.append(pokemon_data)

    paginator = Paginator(pokemons, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(response_base.json())

    context = {
        'pokemons': pokemons,
        'page_obj': page_obj,
        'site_title': 'Pokemons |',
    }

    return render(request, 'pokedex/index.html', context)
