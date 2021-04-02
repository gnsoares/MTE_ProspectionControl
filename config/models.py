#
# IMPORTS
#
# Django
from django.db import models


#
# CODE
#
class Category(models.Model):
    """
    Category model.
    """

    # category information
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name


class ContractType(models.Model):
    """
    ContractType model.
    """

    # contract type information
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Fee(models.Model):
    """
    Fee model.
    """

    # fee information
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class PaymentForm(models.Model):
    """
    PaymentForm model.
    """

    # payment form information
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
