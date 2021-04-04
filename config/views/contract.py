#
# IMPORTS
#
# Python std library
import os

# Django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View


# Project
from config.forms.name import Name
from config.models import ContractType
from prospection_control.views.common_context import COMMON_CONTEXT


#
# CODE
#
class New(View):

    form_class = Name
    template_name = 'name.html'
    title = 'Inclusão de Tipo de Contrato'

    def get(self, request, *args, **kwargs):

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'action': request.path,
                'form': self.form_class(),
                'page_name': self.title,
            },
        )

    def post(self, request, *args, **kwargs):

        # get form data
        form = self.form_class(request.POST)

        # form is valid: create contract type
        if form.is_valid():

            # create contract type object
            contract_type = ContractType(name=form.cleaned_data['name'])

            # save contract type to db
            contract_type.save()

            # render success page
            return HttpResponseRedirect('/config/update/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')

        return HttpResponse(form.errors)


class Edit(View):

    form_class = Name
    template_name = 'name.html'
    title = 'Edição de Tipo de Contrato {0}'

    def get(self, request, id, *args, **kwargs):

        # get contract type by id
        contract_type = ContractType.objects.get(id=id)

        # set form inital data
        form = self.form_class(initial={
            'name': contract_type.name,
        })

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'action': request.path,
                'form': form,
                'page_name': self.title.format(contract_type.name),
            },
        )

    def post(self, request, id, *args, **kwargs):

        # get form data
        form = self.form_class(request.POST)

        # form is valid: create contract type
        if form.is_valid():

            # get contract type by id
            contract_type = ContractType.objects.get(id=id)

            # update contract type information
            contract_type.name = form.cleaned_data['name']

            # save contract type to db
            contract_type.save()

            # render success page
            return HttpResponseRedirect('/config/update/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')

        return HttpResponse(form.errors)


class Remove(View):

    template_name = 'removed.html'
    title = 'Tipo de Contrato {0} Removida'

    def get(self, request, id, *args, **kwargs):

        # get contract type by id
        contract_type = ContractType.objects.get(id=id)

        # remove contract type
        contract_type.delete()

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'page_name': self.title.format(contract_type.name),
            },
        )
