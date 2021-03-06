#
# IMPORTS
#
# Django
from django.urls import path

# Project
from prospection.views.company_close import CompanyClose
from prospection.views.company_edit import CompanyEdit
from prospection.views.company_new import CompanyNew
from prospection.views.company_select import CompanySelect
from prospection.views.prospector_edit import ProspectorEdit
from prospection.views.prospector_new import ProspectorNew
from prospection.views.prospector_select import ProspectorSelect
from prospection.views.success import success


#
# CODE
#
app_name = 'prospection'
urlpatterns = [
    # companies
    path('companies/close/', CompanyClose.as_view(), name='company_close'),
    path('companies/edit/<int:id>/',
         CompanyEdit.as_view(),
         name='company_edit'),
    path('companies/new/', CompanyNew.as_view(), name='company_new'),
    path('companies', CompanySelect.as_view(), name='company_select'),

    # prospectors
    path('prospectors/edit/<int:id>/',
         ProspectorEdit.as_view(),
         name='prospector_edit'),
    path('prospectors/new/', ProspectorNew.as_view(), name='prospector_new'),
    path('prospectors',
         ProspectorSelect.as_view(),
         name='prospector_select'),

    # success
    path('<str:object>/<str:action>/<int:id>/success/',
         success,
         name='success'),
]
