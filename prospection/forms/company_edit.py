#
# IMPORTS
#
# Django
from django import forms

# Project
from prospection.forms.empty_choice import EmptyChoiceField
from prospection.models import Activity, Prospector
from utils import get_choices_from_store


#
# CODE
#
class CompanyEdit(forms.Form):

    name = forms.CharField(max_length=100)

    category = forms.ChoiceField(
        choices=get_choices_from_store('categories')
    )

    main_contact = forms.EmailField(required=False)

    activities = forms.MultipleChoiceField(
        choices=tuple([
            (i, a) for i, a in enumerate(Activity.objects.all().order_by('name'))
        ])
    )

    seller = forms.ModelChoiceField(
        queryset=Prospector.objects.filter(is_seller=True).order_by('name')
    )

    contractor = forms.ModelChoiceField(
        queryset=Prospector.objects.filter(is_contractor=True).order_by(
            'name'
        ),
        required=False
    )

    postseller = forms.ModelChoiceField(
        queryset=Prospector.objects.filter(is_postseller=True).order_by(
            'name'
        ),
        required=False
    )

    fee_type = EmptyChoiceField(choices=get_choices_from_store('fees'),
                                required=False,
                                empty_label='-----')

    contract_type = EmptyChoiceField(
        choices=get_choices_from_store('contracts'),
        required=False,
        empty_label='-----'
    )

    intake = forms.IntegerField(required=False)

    payment_form = EmptyChoiceField(
        choices=get_choices_from_store('payment-forms'),
        required=False,
        empty_label='-----'
    )

    payday = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker4'
            }
        ),
        required=False,
    )

    stand_size = forms.IntegerField(required=False)

    stand_pos = forms.CharField(max_length=100, required=False)

    custom_stand = forms.BooleanField(required=False)

    needs_receipt = forms.BooleanField(required=False)
