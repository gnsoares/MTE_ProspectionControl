#
# IMPORTS
#
# Django
from django.urls import path

# Project
from config.views.category import New as CategoryNew
from config.views.category import Edit as CategoryEdit
from config.views.category import Remove as CategoryRemove
from config.views.contract import New as ContractNew
from config.views.contract import Edit as ContractEdit
from config.views.contract import Remove as ContractRemove
from config.views.fee import New as FeeNew
from config.views.fee import Edit as FeeEdit
from config.views.fee import Remove as FeeRemove
from config.views.payment_form import New as PaymentFormNew
from config.views.payment_form import Edit as PaymentFormEdit
from config.views.payment_form import Remove as PaymentFormRemove
from config.views.update import Update
from prospection.views.activity import New as ActivityNew
from prospection.views.activity import Edit as ActivityEdit
from prospection.views.activity import Remove as ActivityRemove


#
# CODE
#
urlpatterns = [
    path('update/', Update.as_view(), name='update'),

    # activities
    path('activities/new/', ActivityNew.as_view(), name='activity_new'),
    path('activities/edit/<int:id>/',
         ActivityEdit.as_view(),
         name='activity_edit'),
    path('activities/remove/<int:id>/',
         ActivityRemove.as_view(),
         name='activity_remove'),

    # categories
    path('categories/new/', CategoryNew.as_view(), name='category_new'),
    path('categories/edit/<int:id>/',
         CategoryEdit.as_view(),
         name='category_edit'),
    path('categories/remove/<int:id>/',
         CategoryRemove.as_view(),
         name='category_remove'),

    # contracts
    path('contracts/new/', ContractNew.as_view(), name='contract_new'),
    path('contracts/edit/<int:id>/',
         ContractEdit.as_view(),
         name='contract_edit'),
    path('contracts/remove/<int:id>/',
         ContractRemove.as_view(),
         name='contract_remove'),

    # fees
    path('fees/new/', FeeNew.as_view(), name='fee_new'),
    path('fees/edit/<int:id>/', FeeEdit.as_view(), name='fee_edit'),
    path('fees/remove/<int:id>/', FeeRemove.as_view(), name='fee_remove'),

    # payment_forms
    path('payment_forms/new/',
         PaymentFormNew.as_view(),
         name='payment_form_new'),
    path('payment_forms/edit/<int:id>/',
         PaymentFormEdit.as_view(),
         name='payment_form_edit'),
    path('payment_forms/remove/<int:id>/',
         PaymentFormRemove.as_view(),
         name='payment_form_remove'),
]
