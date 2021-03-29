#
# IMPORTS
#
# Django
from django.urls import path

# Project
from .views.prospector_new import ProspectorNew


#
# CODE
#
urlpatterns = [
    # prospectors
    path('prospectors/new/', ProspectorNew.as_view(), name='prospector_new'),
]
