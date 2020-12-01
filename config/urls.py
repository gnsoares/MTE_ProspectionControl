#
# IMPORTS
#
# Django
from django.urls import path

# Project
from config.views.update import Update


#
# CODE
#
app_name = 'config'
urlpatterns = [
    path('update', Update.as_view(), name='update'),
]
