#
# IMPORTS
#
# Django
from django import forms
from django.db.utils import OperationalError

# Project
from prospection.forms.empty_choice import EmptyChoiceField
from prospection.models import Activity, Prospector
from prospection.models import get_choices


#
# CODE
#
class CompanyEdit(forms.Form):

    name = forms.CharField(max_length=100)

    category = forms.ChoiceField(choices=get_choices('categories'))

    main_contact = forms.EmailField(required=False)

    try:
        activities = forms.MultipleChoiceField(
            choices=tuple([
                (i, a)
                for i, a in enumerate(Activity.objects.all().order_by('name'))
            ]),
            required=False
        )

    except OperationalError:
        pass

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

    fee_type = EmptyChoiceField(choices=get_choices('fees'),
                                required=False,
                                empty_label='-----')

    contract_type = EmptyChoiceField(
        choices=get_choices('contracts'),
        required=False,
        empty_label='-----'
    )

    intake = forms.IntegerField(required=False)

    payment_form = EmptyChoiceField(
        choices=get_choices('payment-forms'),
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
