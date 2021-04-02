#
# IMPORTS
#
# Python std library
from os import environ

# Django
from django.core.exceptions import ImproperlyConfigured

# Types
from typing import Any


#
# CODE
#
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
