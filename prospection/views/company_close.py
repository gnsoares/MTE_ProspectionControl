#
# IMPORTS
#
# Python std library
import os
from json.decoder import JSONDecodeError

# Django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View


# Project
from prospection.forms.company_close \
    import CompanyClose as CompanyCloseForm
from prospection.models import Contract
from prospection.utils import get_least_prospector, sheet_update
from prospection_control.views.common_context import COMMON_CONTEXT
from reminders import new_company_reminder
from store import store
from trello import post_card


#
# CODE
#
class CompanyClose(View):

    form_class = CompanyCloseForm
    template_name = 'company_close.html'
    title = 'Fechamento de Empresa'

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

        # form is valid: create company
        if form.is_valid():

            # get company
            company = form.cleaned_data['company']

            # automatic assignment: get prospectors with the least amount
            # of contacts
            if store['automatic-assignment']:
                contractor = get_least_prospector('contractor')
                postseller = get_least_prospector('postseller')

            # not automatic assignment: get from the form
            else:
                contractor = form.cleaned_data['contractor']
                postseller = form.cleaned_data['postseller']

            # create new contract
            contract = Contract(
                company=company,
                fee_type=form.cleaned_data['fee_type'],
                contract_type=form.cleaned_data['contract_type'],
                intake=form.cleaned_data['intake'],
                contractor=contractor,
                postseller=postseller,
            )

            # create card and save its id
            response = post_card(company.name, contractor.list_id_contracts)
            try:
                contract_card = response.json()
            except JSONDecodeError:
                if not os.environ['DEBUG']:
                    return HttpResponse('Something went wrong')
                return HttpResponse(response.status_code, response.text)
            contract.card_id = contract_card['id']

            # save contract to db
            contract.save()

            # save company stage
            company.stage = store['stages']['closed']

            # save company to db
            company.save()

            # inform prospectors of the company assignment
            new_company_reminder(company, contractor, 'contractor')
            new_company_reminder(company, postseller, 'postseller')

            # save in closed companies table
            sheet_update(company)

            # render success page
            return HttpResponseRedirect(f'{request.path}{company.id}/success/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')

        return HttpResponse(form.errors)
