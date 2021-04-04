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
from prospection.forms.company_new import CompanyNew as CompanyNewForm
from prospection.models import Company
from prospection_control.views.common_context import COMMON_CONTEXT
from trello import post_card


#
# CODE
#
class CompanyNew(View):

    form_class = CompanyNewForm
    template_name = 'company_new.html'
    title = 'Inclusão de Empresa'

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

            # create company object
            company = Company(
                name=form.cleaned_data['name'],
                category=form.cleaned_data['category'],
                prospector=form.cleaned_data['seller'],
                main_contact=form.cleaned_data['main_contact']
            )

            # create company card and save its id
            response = post_card(
                company.name,
                form.cleaned_data['seller'].list_id_sales
            )
            try:
                company_card = response.json()
            except JSONDecodeError:
                if not os.environ['DEBUG']:
                    return HttpResponse('Something went wrong')
                return HttpResponse(response.status_code, response.text)
            company.card_id = company_card['id']

            # save company to db
            company.save()

            # render success page
            return HttpResponseRedirect(
                f'{request.path}{company.id}/success/'
            )

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')

        return HttpResponse(form.errors)
