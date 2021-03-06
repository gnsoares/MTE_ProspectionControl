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
class ActivityEdit(forms.Form):

    prospector = forms.ModelChoiceField(
        queryset=Prospector.objects.all().order_by('name')
    )
