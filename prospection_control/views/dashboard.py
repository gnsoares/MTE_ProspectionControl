#
# IMPORTS
#
# Django
from django.shortcuts import render

# Project
from config.models import Category, Fee
from prospection.models import Company, Contract
from prospection_control.views.common_context import COMMON_CONTEXT
from store import store


#
# CODE
#
def dashboard(request):

    title = 'Dashboard'
    template_name = 'index.html'

    categories = {
        'labels': list(Category.objects.all()),
        'data': [
            Company.objects.filter(category=category,
                                   stage=store['stages']['closed']).count()
            for category in Category.objects.all()
        ],
    }

    companies = {
        'total_contact': Company.objects.all().count(),
        'total_closed': Company.objects.filter(
            stage=store['stages']['closed']
        ).count(),
    }

    closed_months = {
        'regulars': [
            Contract.objects.filter(date_closed__month=month).count()
            for month in range(4, 10)
        ],
    }

    fees = [{
        'name': fee.name,
        'count': Contract.objects.filter(fee_type=fee.name).count(),
    } for fee in Fee.objects.all()]

    return render(
        request,
        template_name,
        {
            **COMMON_CONTEXT,
            'page_name': title,
            'companies': companies,
            'fees': fees,
            'categories': categories,
            'closed_months': closed_months,
            'dashboard': True,
        },
    )
