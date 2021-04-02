#
# IMPORTS
#
# Python std library
import os

# Project
from store import store


#
# CODE
#
COMMON_CONTEXT = {
    'contact': os.environ['CONTACT'],
    'contacts_table_url': store['closed-table']['url'],
    'contracts_board_url': store['boards']['contracts']['url'],
    'email_model_url': store['material']['email-model'],
    'manual_url': store['material']['manual'],
    'media_kit_url': store['material']['media-kit'],
    'proposal_url': store['material']['proposal'],
    'sales_board_url': store['boards']['sales']['url'],
    'urls': {
        'prospectors': '/prospection/prospectors',
        'companies': '/prospection/companies',
        'close': '/close/',
        'edit': '/edit/',
        'new': '/new/',
    },
}
