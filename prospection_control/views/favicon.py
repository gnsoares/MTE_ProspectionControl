#
# IMPORTS
#
# Django
from django.http import HttpResponse


#
# CODE
#
def favicon(request):
    return HttpResponse(status=200)
