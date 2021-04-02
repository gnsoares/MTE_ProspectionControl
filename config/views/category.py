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
from config.models import Category
from prospection_control.views.common_context import COMMON_CONTEXT


#
# CODE
#
class New(View):

    form_class = Name
    template_name = 'name.html'
    title = 'Inclusão de Categoria'

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

        # form is valid: create category
        if form.is_valid():

            # create category object
            category = Category(name=form.cleaned_data['name'])

            # save category to db
            category.save()

            # render success page
            return HttpResponseRedirect('/config/update/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')


class Edit(View):

    form_class = Name
    template_name = 'name.html'
    title = 'Edição de Categoria {0}'

    def get(self, request, id, *args, **kwargs):

        # get category by id
        category = Category.objects.get(id=id)

        # set form inital data
        form = self.form_class(initial={
            'name': category.name,
        })

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'action': request.path,
                'form': form,
                'page_name': self.title.format(category.name),
            },
        )

    def post(self, request, id, *args, **kwargs):

        # get form data
        form = self.form_class(request.POST)

        # form is valid: create category
        if form.is_valid():

            # get category by id
            category = Category.objects.get(id=id)

            # update category information
            category.name = form.cleaned_data['name']

            # save category to db
            category.save()

            # render success page
            return HttpResponseRedirect('/config/update/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')


class Remove(View):

    template_name = 'removed.html'
    title = 'Categoria {0} Removida'

    def get(self, request, id, *args, **kwargs):

        # get category by id
        category = Category.objects.get(id=id)

        # remove category
        category.delete()

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'page_name': self.title.format(category.name),
            },
        )
