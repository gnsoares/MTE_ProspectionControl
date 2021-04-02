#
# IMPORTS
#
# Django
from django.shortcuts import render

# Project
from prospection_control.views.common_context import COMMON_CONTEXT
from store import store


#
# CODE
#
def closed_companies(request):

    title = 'Empresas Fechadas'
    template_name = 'closed_companies.html'

    return render(
        request,
        template_name,
        {
            **COMMON_CONTEXT,
            'page_name': title,
            'closed_companies': True,
            'closed_table_url': store['closed-table']['url'],
        },
    )
