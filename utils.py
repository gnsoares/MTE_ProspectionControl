#
# IMPORTS
#
# Python std library
from os import environ

# Django
from django.core.exceptions import ImproperlyConfigured

# Types
from typing import Any

# Project
from store import store


#
# CODE
#
def get_choices_from_store(field: str) -> tuple:
    """
    Get the possible choices for a field from store.
    """
    choices: dict = store[field]['choices']
    return tuple([(k, v) for k, v in choices.items()])


def get_env_var(var: str) -> Any:
    """
    Get the environment variable or return exception.
    """
    # get environment variable
    try:
        return environ[var]

    # could not get environment variable: raise
    except KeyError:
        raise ImproperlyConfigured(f'{var} environment variable is not set!')
