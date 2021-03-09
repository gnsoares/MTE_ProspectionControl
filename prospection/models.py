#
# IMPORTS
#
# Django
from django.db import models


#
# CODE
#
class Prospector(models.Model):
    """
    A prospector is any person in contact with a company.
    """

    # prospector information
    name = models.CharField(max_length=100)
    email = models.EmailField()

    # prospector types
    is_seller = models.BooleanField(default=False)
    is_contractor = models.BooleanField(default=False)
    is_postseller = models.BooleanField(default=False)

    # trello lists ids
    list_id_sales = models.CharField(max_length=100, blank=True, null=True)
    list_id_contracts = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.name
