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
from prospection.forms.activity import Activity as ActivityForm
from prospection.models import Activity
from prospection_control.views.common_context import COMMON_CONTEXT


#
# CODE
#
class New(View):

    form_class = ActivityForm
    template_name = 'activity.html'
    title = 'Inclusão de Atividade'

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

        # form is valid: create activity
        if form.is_valid():

            # create activity object
            activity = Activity(
                name=form.cleaned_data['name'],
                prospector=form.cleaned_data['prospector'],
            )

            # save activity to db
            activity.save()

            # render success page
            return HttpResponseRedirect('/config/update/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')


class Edit(View):

    form_class = ActivityForm
    template_name = 'activity.html'
    title = 'Edição de Atividade {0}'

    def get(self, request, id, *args, **kwargs):

        # get activity by id
        activity = Activity.objects.get(id=id)

        # set form inital data
        form = self.form_class(initial={
            'name': activity.name,
            'prospector': activity.prospector,
        })

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'action': request.path,
                'form': form,
                'page_name': self.title.format(activity.name),
            },
        )

    def post(self, request, id, *args, **kwargs):

        # get form data
        form = self.form_class(request.POST)

        # form is valid: create activity
        if form.is_valid():

            # get activity by id
            activity = Activity.objects.get(id=id)

            # update activity information
            activity.name = form.cleaned_data['name']
            activity.prospector = form.cleaned_data['prospector']

            # save activity to db
            activity.save()

            # render success page
            return HttpResponseRedirect('/config/update/')

        # not debugging: return generic error message
        if not os.environ['DEBUG']:
            return HttpResponse('Something went wrong')


class Remove(View):

    template_name = 'removed.html'
    title = 'Atividade {0} Removida'

    def get(self, request, id, *args, **kwargs):

        # get activity by id
        activity = Activity.objects.get(id=id)

        # remove activity
        activity.delete()

        # render page
        return render(
            request,
            self.template_name,
            {
                **COMMON_CONTEXT,
                'page_name': self.title.format(activity.name),
            },
        )
