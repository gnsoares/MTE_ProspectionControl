#
# IMPORTS
#
# Django
from django.contrib import admin

# Project
from .models import Category
from .models import ContractType
from .models import Fee
from .models import PaymentForm


#
# CODE
#
admin.site.register(Category)
admin.site.register(ContractType)
admin.site.register(Fee)
admin.site.register(PaymentForm)
