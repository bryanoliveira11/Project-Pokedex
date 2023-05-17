from django.shortcuts import render
from .index_view import get_pokemon_data


def pokemon(request, poke_id):
    # validating poke_id in url
    if poke_id > 151:
        poke_id = 1  # poke id back to 1 when > 151

    if poke_id < 1:
        poke_id = 151  # poke id back to 151 when < 1

    try:
        # get the session dict data
        sessionPokemons = request.session.get('pokemon_data', {})

        # data to create other dict for a single pokemon
        pokemon_name = sessionPokemons[str(poke_id)]['name']
        pokemon_image = sessionPokemons[str(poke_id)]['image_default']
        pokemon_type = sessionPokemons[str(poke_id)]['type']
        pokemon_type_img = sessionPokemons[str(poke_id)]['type_img_pokemon']
        pokemon_artwork = sessionPokemons[str(poke_id)]['artwork']
        pokemon_stats = sessionPokemons[str(poke_id)]['stats']

        # creating the dict
        single_pokemon_dict = {
            'poke_id': poke_id,
            'pokemon_name': pokemon_name,
            'pokemon_image': pokemon_image,
            'pokemon_type': pokemon_type,
            'pokemon_type_img': pokemon_type_img,
            'pokemon_artwork': pokemon_artwork,
            'pokemon_stats': pokemon_stats,
        }
        single_pokemon = []
        single_pokemon.append(single_pokemon_dict)

        context = {
            'single_pokemon': single_pokemon,
            'poke_id': poke_id,
            'site_title': f"{pokemon_name} |",
        }

    # doing a request in the poke_id in case of exceptions
    except Exception:
        pokemon_data = get_pokemon_data(poke_id)
        pokemon_id = pokemon_data['id'] 
        pokemon_name = pokemon_data['name']
        pokemon_image = pokemon_data['sprites']['front_default']
        pokemon_type = pokemon_data['types'][0]['type']['name']
        # flake8:noqa
        pokemon_artwork = pokemon_data['sprites']['other']['official-artwork']['front_default']
        
        pokemon_data = {  # creating and inserting data in the dict
                    'poke_id': pokemon_id,
                    'pokemon_name': pokemon_name,
                    'pokemon_image': pokemon_image,
                    'pokemon_artwork': pokemon_artwork,
                    'pokemon_type': pokemon_type,
                    'pokemon_type_img': f"global/poke_types/{pokemon_type}.png",
                    'pokemon_stats': {
                        'hp': pokemon_data['stats'][0]['base_stat'],
                        'attack': pokemon_data['stats'][1]['base_stat'],
                        'defense': pokemon_data['stats'][2]['base_stat'],
                        'sp_attack' : pokemon_data['stats'][3]['base_stat'],
                        'sp_defense': pokemon_data['stats'][4]['base_stat'],
                        'speed': pokemon_data['stats'][5]['base_stat'],
                    }
                }
        
        pokemon = []
        pokemon.append(pokemon_data)  # appending to a list
        
        context = {
            'single_pokemon': pokemon,
            'poke_id': poke_id,
            'site_title': f"{pokemon_name} |",
        }

    return render(request, 'pokedex/pokemon.html', context)
