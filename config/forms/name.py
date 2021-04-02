#
# IMPORTS
#
# Django
from django import forms


#
# CODE
#
class Name(forms.Form):
    name = forms.CharField(max_length=100)
