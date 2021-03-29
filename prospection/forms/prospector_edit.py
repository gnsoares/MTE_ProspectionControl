#
# IMPORTS
#
# Django
from django import forms


#
# CODE
#
class ProspectorEdit(forms.Form):

    email = forms.EmailField()

    is_seller = forms.BooleanField(required=False)

    is_contractor = forms.BooleanField(required=False)

    is_postseller = forms.BooleanField(required=False)
