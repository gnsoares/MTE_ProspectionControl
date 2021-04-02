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
from config.forms.update import Update as UpdateForm
from config.models import Category, ContractType, Fee, PaymentForm
from prospection.models import Activity
from prospection_control.views.common_context import COMMON_CONTEXT
from store import store, update_store


#
# CODE
#
class Update(View):

    form_class = UpdateForm
    template_name = 'update.html'
    title = 'Configuração'

    def get(self, request, *args, **kwargs):

        # set form inital data
        form = self.form_class(initial={
            'attention': store['deadlines']['attention'],
            'urgent': store['deadlines']['urgent'],
            'email_model': store['material']['email-model'],
            'manual': store['material']['manual'],
            'media_kit': store['material']['media-kit'],
            'proposal': store['material']['proposal'],
            'sales_board_id': store['boards']['sales']['id'],
            'sales_board_url': store['boards']['sales']['url'],
            'contracts_board_id': store['boards']['contracts']['id'],
            'contracts_board_url': store['boards']['contracts']['url'],
            'closed_table_id': store['closed-table']['id'],
            'closed_table_range': store['closed-table']['range'],
            'closed_table_url': store['closed-table']['url'],
        })

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'page_name': self.title,
                'form': form,
                'activities': {
                    'new': '/config/activities/new/',
                    'edit': '/config/activities/edit/',
                    'remove': '/config/activities/remove/',
                    'list': [{
                        'count': i + 1,
                        'name': activity.name,
                        'id': activity.id,
                    } for i, activity in enumerate(Activity.objects.all())],
                },
                'categories': {
                    'new': '/config/categories/new/',
                    'edit': '/config/categories/edit/',
                    'remove': '/config/categories/remove/',
                    'list': [{
                        'count': i + 1,
                        'name': category.name,
                        'id': category.id,
                    } for i, category in enumerate(Category.objects.all())],
                },
                'contracts': {
                    'new': '/config/contracts/new/',
                    'edit': '/config/contracts/edit/',
                    'remove': '/config/contracts/remove/',
                    'list': [{
                        'count': i + 1,
                        'name': contract.name,
                        'id': contract.id,
                    } for i, contract in enumerate(
                        ContractType.objects.all()
                    )],
                },
                'fees': {
                    'new': '/config/contracts/new/',
                    'edit': '/config/contracts/edit/',
                    'remove': '/config/contracts/remove/',
                    'list': [{
                        'count': i + 1,
                        'name': fee.name,
                        'id': fee.id,
                    } for i, fee in enumerate(Fee.objects.all())],
                },
                'payment_forms': {
                    'new': '/config/contracts/new/',
                    'edit': '/config/contracts/edit/',
                    'remove': '/config/contracts/remove/',
                    'list': [{
                        'count': i + 1,
                        'name': payment.name,
                        'id': payment.id,
                    } for i, payment in enumerate(PaymentForm.objects.all())],
                },
            },
        )

    def post(self, request, *args, **kwargs):

        # get form data
        form = self.form_class(request.POST)

        # form is valid: create company
        if form.is_valid():

            # save form data in store
            store['deadlines']['attention'] = form.cleaned_data['attention']
            store['deadlines']['urgent'] = form.cleaned_data['urgent']
            store['material']['email-model'] = form.cleaned_data['email_model']
            store['material']['manual'] = form.cleaned_data['manual']
            store['material']['media-kit'] = form.cleaned_data['media_kit']
            store['material']['proposal'] = form.cleaned_data['proposal']
            store['boards']['sales']['id'] = \
                form.cleaned_data['sales_board_id']
            store['boards']['sales']['url'] = \
                form.cleaned_data['sales_board_url']
            store['boards']['contracts']['id'] = \
                form.cleaned_data['contracts_board_id']
            store['boards']['contracts']['url'] = \
                form.cleaned_data['contracts_board_url']
            store['closed-table']['id'] = form.cleaned_data['closed_table_id']
            store['closed-table']['range'] = \
                form.cleaned_data['closed_table_range']
            store['closed-table']['url'] = \
                form.cleaned_data['closed_table_url']

            # update store file
            update_store()

            # render success page
            return HttpResponseRedirect(request.path)

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')
