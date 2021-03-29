#
# IMPORTS
#
# Django
from django import forms

# Project
from prospection.models import Prospector
from utils import get_choices_from_store


#
# CODE
#
class CompanyNew(forms.Form):

    name = forms.CharField(max_length=100)

    category = forms.ChoiceField(choices=get_choices_from_store('categories'))

    seller = forms.ModelChoiceField(
        queryset=Prospector.objects.filter(is_seller=True).order_by('name')
    )

    main_contact = forms.EmailField(required=False)
