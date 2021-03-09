#
# IMPORTS
#
# Django
from django.contrib import admin

# Project
from .models import Activity
from .models import Company
from .models import Prospector


#
# CODE
#
admin.site.register(Activity)
admin.site.register(Company)
admin.site.register(Prospector)
