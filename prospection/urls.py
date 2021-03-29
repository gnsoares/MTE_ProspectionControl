#
# IMPORTS
#
# Django
from django.urls import path

# Project
from .views.company_edit import CompanyEdit
from .views.company_new import CompanyNew
from .views.company_select import CompanySelect
from .views.prospector_edit import ProspectorEdit
from .views.prospector_new import ProspectorNew
from .views.prospector_select import ProspectorSelect


#
# CODE
#
urlpatterns = [
    # companies
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
]
