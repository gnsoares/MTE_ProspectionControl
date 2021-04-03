#
# IMPORTS
#
# Django
from django import forms


#
# CODE
#
class Update(forms.Form):

    automatic_assignment = forms.BooleanField()

    attention = forms.IntegerField()
    urgent = forms.IntegerField()

    email_model = forms.URLField(required=False)
    manual = forms.URLField(required=False)
    media_kit = forms.URLField(required=False)
    proposal = forms.URLField(required=False)

    sales_board_id = forms.CharField(max_length=100, required=False)
    sales_board_url = forms.CharField(max_length=100, required=False)
    contracts_board_id = forms.CharField(max_length=100, required=False)
    contracts_board_url = forms.CharField(max_length=100, required=False)

    closed_table_id = forms.CharField(max_length=100, required=False)
    closed_table_range = forms.CharField(max_length=100, required=False)
    closed_table_url = forms.CharField(max_length=100, required=False)
