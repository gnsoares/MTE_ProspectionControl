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
from prospection.forms.prospector_new import ProspectorNew as ProspectorNewForm
from prospection.models import Prospector
from prospection_control.views.common_context import COMMON_CONTEXT
from store import store
from trello import post_list


#
# CODE
#
class ProspectorNew(View):

    form_class = ProspectorNewForm
    template_name = 'prospector_new.html'
    title = 'Inclusão de Captador'

    def get(self, request, *args, **kwargs):

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'action': request.path,
                'page_name': self.title,
                'form': self.form_class(),
            },
        )

    def post(self, request, *args, **kwargs):

        # get form data
        form = self.form_class(request.POST)

        # form is valid: create prospector
        if form.is_valid():

            # create prospector object
            prospector = Prospector(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                is_seller=form.cleaned_data['is_seller'],
                is_contractor=form.cleaned_data['is_contractor'],
                is_postseller=form.cleaned_data['is_postseller']
            )

            # prospector is seller: create their list and save its id
            if prospector.is_seller:
                response = post_list(
                    prospector.name,
                    store['boards']['sales']['id']
                )
                prospector_sales_list = response.json()
                prospector.list_id_sales = prospector_sales_list['id']

            # prospector is contractor: create their list and save its id
            if prospector.is_contractor:
                response = post_list(
                    prospector.name,
                    store['boards']['contracts']['id']
                )
                prospector_contracts_list = response.json()
                prospector.list_id_contracts = prospector_contracts_list['id']

            # save prospector to db
            prospector.save()

            # render success page
            return HttpResponseRedirect(
                f'{request.path}{prospector.id}/success/'
            )

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')

        return HttpResponse(form.errors)
