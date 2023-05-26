from django.shortcuts import render, redirect
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
        pokemon_name = sessionPokemons[str(poke_id)].get('name')
        pokemon_image = sessionPokemons[str(poke_id)].get('image_default')
        pokemon_type = sessionPokemons[str(poke_id)].get('type')
        pokemon_type_img = sessionPokemons[str(poke_id)].get('type_img_pokemon')
        pokemon_artwork = sessionPokemons[str(poke_id)].get('artwork')
        pokemon_stats = sessionPokemons[str(poke_id)].get('stats')
        
        if not request.get(pokemon_artwork):
            return redirect('pokedex:error')

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
        try:
            pokemon_data = get_pokemon_data(poke_id)
            pokemon_id = pokemon_data.get('id') 
            pokemon_name = pokemon_data.get('name')
            pokemon_image = pokemon_data.get('sprites').get('front_default')
            pokemon_type = pokemon_data.get('types')[0].get('type').get('name')
            # flake8:noqa
            pokemon_artwork = pokemon_data.get('sprites').get('other').get('official-artwork').get('front_default')

            pokemon_data = {  # creating and inserting data in the dict
                        'poke_id': pokemon_id,
                        'pokemon_name': pokemon_name,
                        'pokemon_image': pokemon_image,
                        'pokemon_artwork': pokemon_artwork,
                        'pokemon_type': pokemon_type,
                        'pokemon_type_img': f"global/poke_types/{pokemon_type}.png",
                        'pokemon_stats': {
                            'hp': pokemon_data.get('stats')[0].get('base_stat'),
                            'attack': pokemon_data.get('stats')[1].get('base_stat'),
                            'defense': pokemon_data.get('stats')[2].get('base_stat'),
                            'sp_attack' : pokemon_data.get('stats')[3].get('base_stat'),
                            'sp_defense': pokemon_data.get('stats')[4].get('base_stat'),
                            'speed': pokemon_data.get('stats')[5].get('base_stat'),
                        }
                    }
        except Exception: # return to page error
            return redirect('pokedex:error')
        
        pokemon = []
        pokemon.append(pokemon_data)  # appending to a list
        
        context = {
            'single_pokemon': pokemon,
            'poke_id': poke_id,
            'site_title': f"{pokemon_name} |",
        }

    return render(request, 'pokedex/pokemon.html', context)
