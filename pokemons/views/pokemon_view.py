from django.shortcuts import render, redirect


def pokemon(request, poke_id):
    try:
        sessionPokemons = request.session.get('pokemon_data', {})

        pokemon_name = sessionPokemons[str(poke_id)]['name']
        pokemon_image = sessionPokemons[str(poke_id)]['image_default']
        pokemon_type = sessionPokemons[str(poke_id)]['type']
        pokemon_type_img = sessionPokemons[str(poke_id)]['type_img_pokemon']
        pokemon_artwork = sessionPokemons[str(poke_id)]['artwork']

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
            'single_pokemon': single_pokemon
        }

    except Exception:
        return redirect('pokedex:index')

    return render(request, 'pokedex/pokemon.html', context)
