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
from config.models import PaymentForm
from prospection_control.views.common_context import COMMON_CONTEXT


#
# CODE
#
class New(View):

    form_class = Name
    template_name = 'name.html'
    title = 'Inclusão de Forma de Pagamento'

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

        # form is valid: create payment form
        if form.is_valid():

            # create payment form object
            payment_form = PaymentForm(name=form.cleaned_data['name'])

            # save payment form to db
            payment_form.save()

            # render success page
            return HttpResponseRedirect('/config/update/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')


class Edit(View):

    form_class = Name
    template_name = 'name.html'
    title = 'Edição de Forma de Pagamento {0}'

    def get(self, request, id, *args, **kwargs):

        # get payment form by id
        payment_form = PaymentForm.objects.get(id=id)

        # set form inital data
        form = self.form_class(initial={
            'name': payment_form.name,
        })

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'action': request.path,
                'form': form,
                'page_name': self.title.format(payment_form.name),
            },
        )

    def post(self, request, id, *args, **kwargs):

        # get form data
        form = self.form_class(request.POST)

        # form is valid: create payment form
        if form.is_valid():

            # get payment form by id
            payment_form = PaymentForm.objects.get(id=id)

            # update payment form information
            payment_form.name = form.cleaned_data['name']

            # save payment form to db
            payment_form.save()

            # render success page
            return HttpResponseRedirect('/config/update/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')


class Remove(View):

    template_name = 'removed.html'
    title = 'Forma de Pagamento {0} Removida'

    def get(self, request, id, *args, **kwargs):

        # get payment_form by id
        payment_form = PaymentForm.objects.get(id=id)

        # remove payment_form
        payment_form.delete()

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'page_name': self.title.format(payment_form.name),
            },
        )
