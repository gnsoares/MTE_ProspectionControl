#
# IMPORTS
#
# Python std library
import os

# Third Party
from requests import delete, get, post, put, Response


#
# CONSTANTS
#
API_URL = 'https://api.trello.com/1'
TRELLO_PARAMS = {
    'key': os.environ.get('TRELLO_KEY', ''),
    'token': os.environ.get('TRELLO_TOKEN', ''),
}

# board
BOARD_CARDS = API_URL + '/boards/{0}/cards'

# cards
CARDS = API_URL + '/cards'
CARD = CARDS + '/{0}'
CARD_LABELS = CARD + '/labels'

# lists
LISTS = API_URL + '/lists'
LIST = LISTS + '/{0}'

# labels
LABELS = CARD + '/idLabels'
LABEL = LABELS + '/{0}'


#
# CODE
#
def add_label_to_card(card_id: str, label_id: str) -> Response:
    """
    Add a label to a card.
    """
    # request and return response
    return post(LABELS.format(card_id), params={
        'value': label_id,
        **TRELLO_PARAMS
    })


def get_board_cards(board_id: str) -> Response:
    """
    Get the cards of a board.
    """
    # request and return response
    return get(BOARD_CARDS.format(board_id), params=TRELLO_PARAMS)


def get_card_labels(card_id: str) -> Response:
    """
    Get the labels of a card.
    """
    # request and return response
    return get(CARD_LABELS.format(card_id), params=TRELLO_PARAMS)


def get_card(card_id: str) -> Response:
    """
    Get a card.
    """
    # request and return response
    return get(CARD.format(card_id), params=TRELLO_PARAMS)


def get_list(list_id: str) -> Response:
    """
    Get a list.
    """
    # request and return response
    return get(LIST.format(list_id), params=TRELLO_PARAMS)


def post_card(name: str, list_id: str) -> Response:
    """
    Add a new card in a list.
    """
    # request and return response
    return post(CARDS, params={
        'name': name,
        'idList': list_id,
        **TRELLO_PARAMS
    })


def post_list(name: str, board_id: str) -> Response:
    """
    Add a new list in a board.
    """
    # request and return response
    return post(LISTS, params={
        'name': name,
        'idBoard': board_id,
        **TRELLO_PARAMS
    })


def put_card_in_list(card_id: str, list_id: str) -> Response:
    """
    Update a card in a list.
    """
    # request and return response
    return put(CARD.format(card_id), params={
        'idList': list_id,
        **TRELLO_PARAMS
    })


def remove_card_label(card_id: str, label_id: str) -> Response:
    """
    Remove a label from a card.
    """
    # request and return response
    return delete(LABEL.format(card_id, label_id), params=TRELLO_PARAMS)
