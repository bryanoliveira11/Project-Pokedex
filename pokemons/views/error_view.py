from django.shortcuts import render


def error(request):
    return render(request, 'pokedex/error.html')
