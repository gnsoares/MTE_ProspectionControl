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
from config.models import Fee
from prospection_control.views.common_context import COMMON_CONTEXT


#
# CODE
#
class New(View):

    form_class = Name
    template_name = 'name.html'
    title = 'Inclusão de Cota'

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

        # form is valid: create fee
        if form.is_valid():

            # create fee object
            fee = Fee(name=form.cleaned_data['name'])

            # save fee to db
            fee.save()

            # render success page
            return HttpResponseRedirect('/config/update/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')


class Edit(View):

    form_class = Name
    template_name = 'name.html'
    title = 'Edição de Cota {0}'

    def get(self, request, id, *args, **kwargs):

        # get fee by id
        fee = Fee.objects.get(id=id)

        # set form inital data
        form = self.form_class(initial={
            'name': fee.name,
        })

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'action': request.path,
                'form': form,
                'page_name': self.title.format(fee.name),
            },
        )

    def post(self, request, id, *args, **kwargs):

        # get form data
        form = self.form_class(request.POST)

        # form is valid: create fee
        if form.is_valid():

            # get fee by id
            fee = Fee.objects.get(id=id)

            # update fee information
            fee.name = form.cleaned_data['name']

            # save fee to db
            fee.save()

            # render success page
            return HttpResponseRedirect('/config/update/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')


class Remove(View):

    template_name = 'removed.html'
    title = 'Cota {0} Removida'

    def get(self, request, id, *args, **kwargs):

        # get fee by id
        fee = Fee.objects.get(id=id)

        # remove fee
        fee.delete()

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'page_name': self.title.format(fee.name),
            },
        )
