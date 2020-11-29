#
# IMPORTS
#
# Django
from django.contrib import admin

# Project
from prospection.models import Company
from prospection.models import Prospector


#
# CODE
#
admin.site.register(Company)
admin.site.register(Prospector)
