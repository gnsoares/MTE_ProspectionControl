#
# IMPORTS
#
# Python std library
from json import dumps, load


#
# CONSTANTS
#
STORE_JSON = 'store.json'


#
# CODE
#
store = {}


def get_store() -> dict:
    """
    Configuration store getter.
    """
    # open json and return dict
    try:
        with open(STORE_JSON) as store_file:
            loaded = load(store_file)

    # error opening file: start empty
    except FileNotFoundError:
        loaded = {}

    # update store
    store.update({
        'automatic-assingment': loaded.get('automatic-assingment', True),
        'boards': {
            'sales': {
                'id': loaded.get('boards', {}).get('sales', {}).get('id', ''),
                'url': loaded.get('boards', {}).get('sales', {}).get('url',
                                                                     '#'),
            },
            'contracts': {
                'id': loaded.get('boards', {}).get('contracts', {}).get('id',
                                                                        ''),
                'url': loaded.get('boards', {}).get('contracts', {}).get('url',
                                                                         '#'),
            },
        },
        'closed-table': {
            'id': loaded.get('closed-table', {}).get('id', ''),
            'range': loaded.get('closed-table', {}).get('range',
                                                        'Página1!1:1000'),
            'url': loaded.get('closed-table', {}).get('url', '#'),
        },
        'deadlines': {
            'attention': loaded.get('deadlines', {}).get('attention', 8),
            'urgent': loaded.get('deadlines', {}).get('urgent', 15),
        },
        'material': {
            'email-model': loaded.get('material', {}).get('email-model', '#'),
            'manual': loaded.get('material', {}).get('manual', '#'),
            'media-kit': loaded.get('material', {}).get('media-kit', '#'),
            'proposal': loaded.get('material', {}).get('proposal', '#'),
        },
        'stages': {
            'initial': 'INIT',
            'closed': 'CLOS',
        },
    })


def update_store() -> dict:
    """
    Configuration store updater.
    """
    # open json and return dict
    with open(STORE_JSON, 'w') as store_file:
        store_file.write(dumps(store))
