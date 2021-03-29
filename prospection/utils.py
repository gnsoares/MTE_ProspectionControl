#
# IMPORTS
#
# Python std library
from random import choice

# Project
from .models import Company, Prospector
from trello import add_label_to_card, get_board_cards, remove_card_label
from utils import get_store


#
# CODE
#
def get_least_prospector(function: str) -> Prospector:
    """
    Get a prospector with the least amount of contacts.
    """
    least_contact_count = sorted(
        Prospector.objects.filter(**{f'is_{function}': True}),
        key=lambda prospector: prospector.contact_count
    )[0].contact_count
    bottom_prospectors = list(filter(
        lambda prospector: prospector.contact_count == least_contact_count,
        Prospector.objects.all()
    ))
    return choice(bottom_prospectors)


def label_update(board_id: str) -> None:
    """
    Update status labels of the cards of a board.
    """
    # get configuration store
    store = get_store()

    # get board cards
    cards = get_board_cards(board_id).json()

    # update all cards
    for card in cards:

        # get card company
        try:
            company = Company.objects.get(card_id=card['id'])
        except Company.DoesNotExist:
            continue

        # get card labels
        labels = card['labels']
        label_ids = [label['id'] for label in labels]

        # see if this card has only the right label
        found = False
        for label in ['updated', 'attention', 'urgent']:

            # status label in card: check if it is the right one
            if store['labels'][label]['id'] in label_ids:

                # not the right one: remove it
                if label != company.status_label:
                    remove_card_label(card['id'], label['id'])

                # right one: set flag
                else:
                    found = True

        # not found right label: add it
        if not found:
            add_label_to_card(card['id'],
                              store['labels'][company.status_label]['id'])
