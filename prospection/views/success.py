#
# IMPORTS
#
# Django
from django.shortcuts import render


# Project
from prospection.models import Company, Prospector
from prospection_control.views.common_context import COMMON_CONTEXT


#
# CONTANTS AND DEFINITIONS
#
ACTION_TRANSLATOR = {
    'close': {
        'infinitive': 'Fechar',
        'title': 'Fechamento',
        'past': 'fechada',
    },
    'edit': {
        'infinitive': 'Editar',
        'title': 'Edição',
        'past': 'editado(a)',
    },
    'new': {
        'infinitive': 'Adicionar',
        'title': 'Adição',
        'past': 'adicionado(a)',
    },
}
OBJECT_TRANSLATOR = {
    'companies': {
        'title': 'Empresa',
        'do_more': 'a empresa',
    },
    'prospectors': {
        'title': 'Captador',
        'do_more': 'o(a) captador(a)',
    },
}
SELECTORS = {
    'companies': lambda id: Company.objects.get(id=id).name,
    'prospectors': lambda id: Prospector.objects.get(id=id).name,
}


#
# CODE
#
def success(request, object: str, action: str, id: int):

    title = f'{ACTION_TRANSLATOR[action]["title"]} de ' \
            f'{OBJECT_TRANSLATOR[object]["title"]}'
    template_name = 'success.html'

    # render page
    return render(
        request,
        template_name,
        {
            **COMMON_CONTEXT,
            'page_name': title,
            'message': f'{SELECTORS[object](id)} '
                       f'{ACTION_TRANSLATOR[action]["past"]} com sucesso!',
            'do_more': {
                'url': f'/prospection/{object}' +
                       '/action' if action != 'edit' else '',
                'text': f'{ACTION_TRANSLATOR[action]["infinitive"]} '
                        f'outr{OBJECT_TRANSLATOR[object]["do_more"]}',
            },
        },
    )
