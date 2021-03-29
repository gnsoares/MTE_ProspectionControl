#
# IMPORTS
#
# Django
from django import forms
from django_select2.forms import ModelSelect2Widget

# Project
from prospection.models import Company, Prospector
from prospection.models import get_choices
from store import store


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
            stage=store['stages']['closed']
        ).order_by('name'),
    )

    fee_type = forms.ChoiceField(choices=get_choices('fees'))

    contract_type = forms.ChoiceField(choices=get_choices('contracts'))

    intake = forms.IntegerField()

    if not store['automatic-assignment']:
        contractor = forms.ModelChoiceField(
            queryset=Prospector.objects.filter(is_contractor=True).order_by(
                'name'
            )
        )
        postseller = forms.ModelChoiceField(
            queryset=Prospector.objects.filter(is_postseller=True).order_by(
                'name'
            )
        )
