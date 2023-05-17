from django.shortcuts import render, redirect


def pokemon(request, poke_id):

    if poke_id > 151 or poke_id < 1:  # validating poke_id in url
        return redirect('pokedex:index')

    try:
        # get the session dict data
        sessionPokemons = request.session.get('pokemon_data', {})

        # data to create other dict for a single pokemon
        pokemon_name = sessionPokemons[str(poke_id)]['name']
        pokemon_image = sessionPokemons[str(poke_id)]['image_default']
        pokemon_type = sessionPokemons[str(poke_id)]['type']
        pokemon_type_img = sessionPokemons[str(poke_id)]['type_img_pokemon']
        pokemon_artwork = sessionPokemons[str(poke_id)]['artwork']

        # creating the dict
        single_pokemon_dict = {
            'poke_id': poke_id,
            'pokemon_name': pokemon_name,
            'pokemon_image': pokemon_image,
            'pokemon_type': pokemon_type,
            'pokemon_type_img': pokemon_type_img,
            'pokemon_artwork': pokemon_artwork,
        }

        single_pokemon = []
        single_pokemon.append(single_pokemon_dict)

        context = {
            'single_pokemon': single_pokemon,
            'poke_id': poke_id,
            'site_title': f"{pokemon_name} |",
        }

    # return to error page in case of problem when requesting
    except Exception:
        return redirect('pokedex:error')

    return render(request, 'pokedex/pokemon.html', context)
