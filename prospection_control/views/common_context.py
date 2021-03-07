#
# IMPORTS
#
# Python std library
import os

# Project
from utils import get_store


#
# CODE
#


COMMON_CONTEXT = {
    'contact': os.environ['CONTACT'],
    'contacts_table_url': get_store()['closed-table']['url'],
    'contracts_board_url': get_store()['boards']['contracts']['url'],
    'email_model_url': get_store()['material']['email-model'],
    'manual_url': get_store()['material']['manual'],
    'media_kit_url': get_store()['material']['media-kit'],
    'proposal_url': get_store()['material']['proposal'],
    'sales_board_url': get_store()['boards']['sales']['url'],
}
