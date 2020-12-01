#
# IMPORTS
#
# Django
from django.urls import path

# Project
from core.views import (CloseCompany,
                        EditCompany,
                        EditProspector,
                        NewCompany,
                        NewProspector,
                        SelectCompany,
                        SelectProspector,
                        success)


#
# CODE
#
app_name = 'core'
urlpatterns = [
    # close
    path('close_company/', CloseCompany.as_view(), name='close_company'),

    # edit
    path('edit_company/<int:id>/',
         EditCompany.as_view(),
         name='edit_company'),
    path('edit_prospector/<int:id>/',
         EditProspector.as_view(),
         name='edit_prospector'),

    # new
    path('new_company/', NewCompany.as_view(), name='new_company'),
    path('new_prospector/', NewProspector.as_view(), name='new_prospector'),

    # select
    path('select_company/', SelectCompany.as_view(), name='select_company'),
    path('select_prospector/',
         SelectProspector.as_view(),
         name='select_prospector'),

    # success
    path('<str:action>_<str:object>/<int:id>/success/',
         success,
         name='success'),
]
