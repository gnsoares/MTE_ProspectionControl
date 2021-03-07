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
from captacao_talento.views.common_context import COMMON_CONTEXT
from prospection.forms.company_edit \
    import CompanyEdit as CompanyEditForm
from prospection.models import Company, Contract
from utils import get_store


#
# CODE
#
class CompanyEdit(View):

    form_class = CompanyEditForm
    template_name = 'company_edit.html'
    title = 'Edição de {0}'

    def get(self, request, id, *args, **kwargs):

        # get company by id and its contract
        company = Company.objects.get(id=id)
        try:
            contract = Contract.objects.get(company=company)
        except Contract.DoesNotExist:
            contract = None

        # set form inital data
        initial = {
            'name': company.name,
            'category': company.category,
            'main_contact': company.main_contact,
            'seller': company.prospector,
        }
        if contract is not None:
            initial.update({
                'contractor': contract.contractor,
                'postseller': contract.postseller,
                'fee_type': contract.fee_type,
                'contract_type': contract.contract_type,
                'intake': contract.intake,
                'payment_form': contract.payment_form,
                'payday': contract.payday,
                'stand_size': contract.stand_size,
                'stand_pos': contract.stand_pos,
                'custom_stand': contract.custom_stand,
                'needs_receipt': contract.needs_receipt,
            })
        form = self.form_class(initial=initial)

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'page_name': self.title.format(company.name),
                'action': request.path,
                'is_closed': company.stage == get_store()['stages']['closed'],
                'form': form,
            },
        )

    def post(self, request, id, *args, **kwargs):

        # get form data
        form = self.form_class(request.POST)

        # form is valid: create company
        if form.is_valid():

            # get company by id and its contract
            company = Company.objects.get(id=id)
            try:
                contract = Contract.objects.get(company=company)
            except Contract.DoesNotExist:
                contract = None

            # company has a new seller anymore: deal with it
            if company.prospector != form.cleaned_data['seller']:
                # TODO: move company card
                pass

            # company has a new contractor anymore: deal with it
            if contract is not None and \
               contract.contractor != form.cleaned_data['contractor']:
                # TODO: move company card
                pass

            # update company values
            company.name = form.cleaned_data['name']
            company.category = form.cleaned_data['category']
            company.main_contact = form.cleaned_data['main_contact']
            company.prospector = form.cleaned_data['seller']

            # update contract values
            if contract is not None:
                contract.contractor = form.cleaned_data['contractor']
                contract.postseller = form.cleaned_data['postseller']
                contract.fee_type = form.cleaned_data['fee_type']
                contract.contract_type = form.cleaned_data['contract_type']
                contract.intake = form.cleaned_data['intake']
                contract.payment_form = form.cleaned_data['payment_form']
                contract.payday = form.cleaned_data['payday']
                contract.stand_size = form.cleaned_data['stand_size']
                contract.stand_pos = form.cleaned_data['stand_pos']
                contract.custom_stand = form.cleaned_data['custom_stand']
                contract.needs_receipt = form.cleaned_data['needs_receipt']

            # save company and its contract to db
            company.save()
            contract.save()

            # render success page
            return HttpResponseRedirect(f'{request.path}success/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')
