from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import requests
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=256, ttl=3600)  # creating cache


@cached(cache)  # saving results in cache
def get_pokemon_data(pokemon_name):
    endpoint_pokemon = requests.get(  # getting a unique pokemon using name
            f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
            )
    return endpoint_pokemon.json()


def index(request):
    MAX_OFFSET = 150  # max offset in api
    LIMIT = 15  # limit per page / number to advance in endpoint
    LIMIT_REVERSE = (LIMIT * -1)

    offset = int(request.GET.get('offset', 0))

    if not offset % LIMIT == 0 or offset > MAX_OFFSET:  # validating offset
        return redirect('pokedex:index')

    # creating key 'pokemon_data' in the session 
    if not request.session.get('pokemon_data'):
        request.session['pokemon_data'] = {}

    session_pokemon_data = request.session['pokemon_data']

    try:
        # base endpoint to get pokemons
        endpoint_base = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/?limit={LIMIT}&offset={offset}"
            )

        results = endpoint_base.json()['results']  # getting the results key

        pokemons = []

        for result in results:
            pokemon_name = result['name']

            # getting pokemon data
            pokemon_data = get_pokemon_data(pokemon_name)
            pokemon_id = pokemon_data['id']  # getting the id
            pokemon_image = pokemon_data['sprites']['front_default']  # getting the image
            pokemon_type = pokemon_data['types'][0]['type']['name']  # getting the name
            # flake8:noqa
            pokemon_artwork = pokemon_data['sprites']['other']['official-artwork']['front_default']

            pokemon_data = {  # creating and inserting data in the dict
                    'poke_id': pokemon_id,
                    'name': pokemon_name,
                    'image_default': pokemon_image,
                    'artwork': pokemon_artwork,
                    'type': pokemon_type,
                    'type_img_index': f"global/imgs/{pokemon_type}.png",
                    'type_img_pokemon': f"global/poke_types/{pokemon_type}.png",
                    'stats': {
                        'hp': pokemon_data['stats'][0]['base_stat'],
                        'attack': pokemon_data['stats'][1]['base_stat'],
                        'defense': pokemon_data['stats'][2]['base_stat'],
                        'sp_attack' : pokemon_data['stats'][3]['base_stat'],
                        'sp_defense': pokemon_data['stats'][4]['base_stat'],
                        'speed': pokemon_data['stats'][5]['base_stat'],
                    }
                }
            pokemons.append(pokemon_data)  # appending to a list
            session_pokemon_data[pokemon_id] = pokemon_data # appending data in the session key dict
            
    except Exception: # redirecting to an error url if the api is not working
        return redirect('pokedex:error')
    
    request.session['pokemon_data'] = session_pokemon_data # saving data in the session key
    request.session.save()
    
    # paginator and calculating the number of pages
    paginator = Paginator(pokemons, 1)
    paginator.count = int(MAX_OFFSET / LIMIT) + 1
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if offset == MAX_OFFSET:  # using pop to remove pokemons that i didn't want
        for i in range(14):
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
