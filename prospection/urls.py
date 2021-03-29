#
# IMPORTS
#
# Django
from django.urls import path

# Project
from .views.prospector_edit import ProspectorEdit
from .views.prospector_new import ProspectorNew
from .views.prospector_select import ProspectorSelect


#
# CODE
#
urlpatterns = [
    # prospectors
    path('prospectors/edit/<int:id>/',
         ProspectorEdit.as_view(),
         name='prospector_edit'),
    path('prospectors/new/', ProspectorNew.as_view(), name='prospector_new'),
    path('prospectors',
         ProspectorSelect.as_view(),
         name='prospector_select'),
]
