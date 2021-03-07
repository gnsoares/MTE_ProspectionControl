#
# IMPORTS
#
# Django
from django.shortcuts import render
from django.views import View


# Project
from captacao_talento.views.common_context import COMMON_CONTEXT
from prospection.models import Prospector


#
# CODE
#
class ProspectorSelect(View):

    template_name = 'prospector_select.html'
    title = 'Seleção de Captador'

    def get(self, request, *args, **kwargs):

        # get all prospectors sorted by name
        prospectors = list(Prospector.objects.all().order_by('name'))

        # process prospectors functions and count
        counter = 1
        for prospector in prospectors:

            # initiate with empty functions
            functions = []

            # prospector is seller: append human readable function
            if prospector.is_seller:
                functions.append('Vendas')

            # prospector is contractor: append human readable function
            if prospector.is_contractor:
                functions.append('Contratos')

            # prospector is postseller: append human readable function
            if prospector.is_seller:
                functions.append('Pós-Vendas')

            # construct human readable function list
            if len(functions) <= 1:
                prospector.functions = ''.join(functions)
            else:
                prospector.functions = \
                    f'{", ".join(functions[:-1])} e {functions[-1]}'

            # assign prospector count and update the counter
            prospector.count = counter
            counter += 1

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'action': request.path,
                'edit': 'prospectors/edit/',
                'page_name': self.title,
                'prospectors': prospectors,
            },
        )
