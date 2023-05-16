from django.template import Library
from utils import utils

register = Library()


@register.filter
def format_id(poke_id):
    return utils.format_id(poke_id)
