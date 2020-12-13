#
# IMPORTS
#
# Django
from django.contrib import admin

# Project
from prospection.models import Activity
from prospection.models import Company
from prospection.models import Contract
from prospection.models import Prospector


#
# CODE
#
admin.site.register(Activity)
admin.site.register(Company)
admin.site.register(Contract)
admin.site.register(Prospector)
