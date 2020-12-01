#
# IMPORTS
#
# Django
from django.shortcuts import render


#
# CODE
#
def success(request):
    return render(request, '', {})
