from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import requests


def index(request):
    MAX_OFFSET = 144  # max offset in api
    LIMIT = 16  # limit per page / number to advance in endpoint
    LIMIT_REVERSE = (LIMIT * -1)

    offset = int(request.GET.get('offset', 0))

    if not offset % 16 == 0 or offset > MAX_OFFSET:  # validating offset
        return redirect('pokedex:index')

    # base endpoint to get pokemons
    endpoint_base = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/?limit={LIMIT}&offset={offset}"
        )

    results = endpoint_base.json()['results']  # getting the results key

    pokemons = []

    for result in results:
        pokemon_name = result['name']

        endpoint_pokemon = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
            )

        pokemon_image = endpoint_pokemon.json()['sprites']['front_default']
        pokemon_id = endpoint_pokemon.json()['id']

        pokemon_data = {  # inserting data in the dict
                'poke_id': pokemon_id,
                'name': pokemon_name,
                'image_default': pokemon_image,
            }

        pokemons.append(pokemon_data)  # appending to a list

    # paginator and calculating the number of pages
    paginator = Paginator(pokemons, 1)
    paginator.count = int(MAX_OFFSET / LIMIT) + 1
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if offset == MAX_OFFSET:  # using pop to remove pokemons that i didn't want
        for i in range(9):
            pokemons.pop()

    context = {
        'pokemons': pokemons,
        'page_obj': page_obj,
        'site_title': 'Pokemons |',
        'offset': offset,
        'max_offset': MAX_OFFSET,
        'limit': LIMIT,
        'limit_reverse': LIMIT_REVERSE,
    }

    return render(request, 'pokedex/index.html', context)
