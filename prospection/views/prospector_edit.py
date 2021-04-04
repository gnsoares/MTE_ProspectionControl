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
from prospection.forms.prospector_edit \
    import ProspectorEdit as ProspectorEditForm
from prospection.models import Company, Contract, Prospector
from prospection.utils import get_least_prospector
from prospection_control.views.common_context import COMMON_CONTEXT
from reminders import new_company_reminder
from store import store
from trello import post_list, put_card_in_list


#
# CODE
#
class ProspectorEdit(View):

    form_class = ProspectorEditForm
    template_name = 'prospector_edit.html'
    title = 'Edição de {0}'

    def get(self, request, id, *args, **kwargs):

        # get prospector by id
        prospector = Prospector.objects.get(id=id)

        # set form inital data
        form = self.form_class(initial={
            'email': prospector.email,
            'is_seller': prospector.is_seller,
            'is_contractor': prospector.is_contractor,
            'is_postseller': prospector.is_postseller,
        })

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'page_name': self.title.format(prospector.name),
                'action': request.path,
                'form': form,
            },
        )

    def post(self, request, id, *args, **kwargs):

        # get form data
        form = self.form_class(request.POST)

        # form is valid: create prospector
        if form.is_valid():

            # get prospector by id
            prospector = Prospector.objects.get(id=id)

            # prospector is not a seller anymore: deal with it
            if prospector.is_seller and not form.cleaned_data['is_seller']:

                # assign each company to a new seller and notify them
                for company in Company.objects.filter(prospector=prospector):
                    new = get_least_prospector('seller')
                    put_card_in_list(company.card_id, new.list_id_sales)
                    new_company_reminder(company, new, 'seller')

            # prospector is now seller: create their list and save its id
            if not prospector.is_seller and form.cleaned_data['is_seller']:
                response = post_list(
                    prospector.name,
                    store['boards']['sales']['id']
                )
                prospector_sales_list = response.json()
                prospector.list_id_sales = prospector_sales_list['id']

            # prospector is not a contractor anymore: deal with it
            if prospector.is_contractor and \
               not form.cleaned_data['is_contractor']:

                # assign each company to a new contractor and notify them
                for company in Contract.objects.filter(contractor=prospector):
                    new = get_least_prospector('contractor')
                    put_card_in_list(company.card_id, new.list_id_contracts)
                    new_company_reminder(company, new, 'contractor')

            # prospector is now contractor: create their list and save its id
            if not prospector.is_contractor and \
               form.cleaned_data['is_contractor']:
                response = post_list(
                    prospector.name,
                    store['boards']['contracts']['id']
                )
                prospector_contracts_list = response.json()
                prospector.list_id_contracts = prospector_contracts_list['id']

            # prospector is not a contractor anymore: deal with it
            if prospector.is_postseller and \
               not form.cleaned_data['is_postseller']:

                # assign each company to a new postseller and notify them
                for company in Contract.objects.filter(postseller=prospector):
                    new = get_least_prospector('postseller')
                    new_company_reminder(company, new, 'postseller')

            # update prospector values
            prospector.email = form.cleaned_data['email']
            prospector.is_seller = form.cleaned_data['is_seller']
            prospector.is_contractor = form.cleaned_data['is_contractor']
            prospector.is_postseller = form.cleaned_data['is_postseller']

            # save prospector to db
            prospector.save()

            # render success page
            return HttpResponseRedirect(f'{request.path}success/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')

        return HttpResponse(form.errors)
