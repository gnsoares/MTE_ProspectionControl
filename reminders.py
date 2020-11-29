#
# IMPORTS
#
# Python std library
import os

# Django
from django.core.mail import send_mail

# Project
from prospection.models import Company, Prospector


#
# CONSTANTS
#
FROM_EMAIL = os.environ.get('EMAIL_HOST_USER', '')
SUBJECT = '[Talento 2021]'
GREETING = 'Olá, {0}!\n'
SIGNATURE = ''.join(['\nQualquer dúvida ou problema favor entrar  ',
                     f'em contatopelo endereço {FROM_EMAIL}'])
FUNCTION = {
    'contract': 'o contrato.\n',
    'postsale': 'a exposição.\n',
}


#
# CODE
#
def new_company_reminder(
    company: Company,
    prospector: Prospector,
    function: str
):
    """
    E-mail reminder for a prospector that received a new company.
    """

    # set message subject
    subject = f'{SUBJECT} Alerta de nova empresa'

    # set message body
    body = ''.join([
        f'A empresa {company} acabou de ser fechada. Agora você precisa ',
        'discutir com o(a) representante da empresa os detalhes d',
        FUNCTION[function],
        f'\nPode usar o e-mail {company.main_contact} para entrar em ',
        'contato\n',
        '\nQuando tudo estiver definido, vá até a plataforma e clique em ',
        'Editar Empresa para registrar as informações.',
    ])

    # format message
    message = '\n' \
              .join([GREETING, body, SIGNATURE]) \
              .format(prospector.name)

    # set html message body
    html_body = ''.join([
        f'A empresa <b><i>{company}</i></b> acabou de ser fechada. Agora '
        'você precisa discutir com o(a) representante da empresa os '
        'detalhes d',
        FUNCTION[function],
        f'<br>Pode usar o e-mail {company.main_contact} para entrar em ',
        'contato<br>',
        '<br>Quando tudo estiver definido, vá até a plataforma e clique em ',
        '<b><i>Editar Empresa</i></b> para registrar as informações.',
    ])

    # format html message
    html_message = '<br>' \
                   .join([GREETING, html_body, SIGNATURE]) \
                   .format(prospector.name) \
                   .replace('\n', '<br>')

    # set recipients
    recipient_list = [prospector.email]

    # send mail
    return send_mail(subject,
                     message,
                     FROM_EMAIL,
                     recipient_list,
                     html_message=html_message)


def wrong_prospector_added(name: str):
    """
    E-mail reminder for a wrong prospector added.
    """

    # set message subject
    subject = f'{SUBJECT} Uso incorreto da plataforma'

    # set message body
    message = f'{name} criou uma lista manualmente!'

    # set recipients
    recipient_list = [os.environ['CONTACT']]

    # send mail
    return send_mail(subject, message, FROM_EMAIL, recipient_list)


def wrong_company_added(company: Company, prospector: Prospector):
    """
    E-mail reminder for a wrong company added.
    """

    # set message subject
    subject = f'{SUBJECT} Uso incorreto da plataforma'

    # set message body
    body = ''.join([
        f'Você tentou adicionar a empresa {company}, mas o fez da ',
        'maneira errada! Por favor vá até a plataforma e clique em ',
        'Adicionar Empresa para resolver esse problema.'
    ])

    # format message
    message = '\n' \
              .join([GREETING, body, SIGNATURE]) \
              .format(prospector.name)

    # set html message body
    html_body = ''.join([
        f'Você tentou adicionar a empresa <b><i>{company}</i></b>, mas o fez ',
        'da maneira errada! Por favor vá até a plataforma e clique em ',
        '<b><i>Adicionar Empresa</i></b> para resolver esse problema.',
    ])

    # format html message
    html_message = '<br>' \
                   .join([GREETING, html_body, SIGNATURE]) \
                   .format(prospector.name) \
                   .replace('\n', '<br>')

    # set recipients
    recipient_list = [prospector.email]

    # send mail
    return send_mail(subject,
                     message,
                     FROM_EMAIL,
                     recipient_list,
                     html_message=html_message)


def wrong_company_closed(company: Company):
    """
    E-mail reminder for a wrong company closed.
    """

    # set message subject
    subject = f'{SUBJECT} Uso incorreto da plataforma'

    # set message body
    body = ''.join([
        f'Você tentou fechar a empresa {company}, mas o fez da maneira ',
        'errada! Por favor vá até a plataforma e clique em Fechar Empresa ',
        'para resolver esse problema.',
    ])

    # format message
    html_body = ''.join([
        f'Você tentou fechar a empresa <i>{company}</i>, mas o fez da ',
        'maneira errada! Por favor vá até a plataforma e clique em ',
        '<b><i>Fechar Empresa</i></b> para resolver esse problema.',
    ])

    # set html message body
    message = '\n' \
              .join([GREETING, body, SIGNATURE]) \
              .format(company.prospector.name)

    # format html message
    html_message = '<br>' \
                   .join([GREETING, html_body, SIGNATURE]) \
                   .format(company.prospector.name) \
                   .replace('\n', '<br>')

    # set recipients
    recipient_list = [company.prospector.email]

    # send mail
    return send_mail(subject,
                     message,
                     FROM_EMAIL,
                     recipient_list,
                     html_message=html_message)


def contact_reminder(prospector: Prospector):
    """
    E-mail reminder to contact companies.
    """

    # set message subject
    subject = f'{SUBJECT} Lembrete de Captação'

    # set message body
    body = 'Você precisa entrar em contato com a(s) empresa(s) a seguir:'
    companies = [
        f'\t* {c.name} ({c.main_contact});'
        for c in prospector.contact_list
        if c.needs_reminder
    ]

    # format message
    message = '\n' \
              .join([GREETING, body, *companies, SIGNATURE]) \
              .format(prospector.name)

    # set recipients
    recipient_list = [prospector.email]

    # send mail
    return send_mail(subject, message, FROM_EMAIL, recipient_list)
