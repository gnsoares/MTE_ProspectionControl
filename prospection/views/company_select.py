#
# IMPORTS
#
# Django
from django.shortcuts import render
from django.views import View


# Project
from prospection_control.views.common_context import COMMON_CONTEXT
from prospection.models import Company


#
# CODE
#
class CompanySelect(View):

    template_name = 'company_select.html'
    title = 'Seleção de Empresa'

    def get(self, request, *args, **kwargs):

        # get all companies sorted by name
        companies = list(Company.objects.all().order_by('name'))

        # process companies count
        counter = 0
        for company in companies:

            # assign company count and update the counter
            company.count = counter
            counter += 1

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'action': request.path,
                'edit': 'companies/edit/',
                'page_name': self.title,
                'companies': companies,
            },
        )
