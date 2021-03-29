#
# IMPORTS
#
# Python std library
from random import choice

# Project
from .models import Prospector


#
# CODE
#
def get_least_prospector(function: str) -> Prospector:
    """
    Get a prospector with the least amount of contacts.
    """
    least_contact_count = sorted(
        Prospector.objects.filter(**{f'is_{function}': True}),
        key=lambda prospector: prospector.contact_count
    )[0].contact_count
    bottom_prospectors = list(filter(
        lambda prospector: prospector.contact_count == least_contact_count,
        Prospector.objects.all()
    ))
    return choice(bottom_prospectors)
