#
# IMPORTS
#
# Django
from django import forms

# Project
from prospection.models import Prospector


#
# CODE
#
class Activity(forms.Form):

    name = forms.CharField(max_length=100)

    prospector = forms.ModelChoiceField(
        queryset=Prospector.objects.all().order_by('name')
    )
