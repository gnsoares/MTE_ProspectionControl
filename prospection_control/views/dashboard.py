#
# IMPORTS
#
# Django
from django.shortcuts import render


#
# CODE
#
def dashboard(request):
    template_name = "index.html"
    return render(request, template_name, {})
