#
# IMPORTS
#
# Django
from django import forms
from django_select2.forms import ModelSelect2Widget

# Project
from prospection.models import Company
from utils import get_choices_from_store, get_store


#
# CODE
#
class CompanyClose(forms.Form):

    company = forms.ModelChoiceField(
        widget=ModelSelect2Widget(
            model=Company,
            search_fields=['name__icontains']
        ),
        queryset=Company.objects.exclude(
            seller_stage=get_store()['stages']['closed']
        ).order_by('name'),
    )

    fee_type = forms.ChoiceField(choices=get_choices_from_store('fees'))

    contract_type = forms.ChoiceField(
        choices=get_choices_from_store('contracts')
    )

    intake = forms.IntegerField()
