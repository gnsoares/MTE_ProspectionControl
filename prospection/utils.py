#
# IMPORTS
#
# Python std library
from os import path
import pickle
from random import choice

# Google Sheets API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Project
from .models import Company, Prospector
from store import store
from trello import add_label_to_card, get_board_cards, remove_card_label


#
# CODE
#
def get_least_prospector(function: str) -> Prospector:
    """
    Get a prospector with the least amount of contacts.
    """
    # get the number of contacts of the prospector with the least contacts
    least_contact_count = sorted(
        Prospector.objects.filter(**{f'is_{function}': True}),
        key=lambda prospector: prospector.contact_count
    )[0].contact_count

    # get all prospectors with the lowest count
    bottom_prospectors = list(filter(
        lambda prospector: prospector.contact_count == least_contact_count,
        Prospector.objects.filter(**{f'is_{function}': True})
    ))

    # return a random prospector with the lowest count
    return choice(bottom_prospectors)


def label_update(board_id: str) -> None:
    """
    Update status labels of the cards of a board.
    """
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


def sheet_update(company):
    """
    Update the spreadsheet of the closed companies.
    """
    # get spreadsheet and API information
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = store['closed-table']['id']
    RANGE_NAME = store['closed-table']['range']
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # call the Sheets API
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # get spreadsheet
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()

    # get spreadsheet values
    values = result.get('values', [])

    # get company information
    row = [
        company.name,
        company.category,
        company.main_contact,
        company.seller.name,
        company.contract.contractor.name,
        company.contract.postseller.name,
        company.contract.fee_type,
        company.contract.contract_type,
        company.contract.intake,
        company.contract.payment_form,
        (company.contract.payday.strftime('%d/%m/%Y')
         if company.contract.payday
         else ''),
        company.contract.stand_size,
        company.contract.stand_pos,
        company.contract.custom_stand,
        company.contract.needs_receipt,
    ]

    # company is in the sheet: update values in the correct row
    for i, value in enumerate(values):
        if value[0] == company.name:
            values[i] = row
            break

    # company not in the sheet put in new row
    else:
        values.append(row)

    # update sheet
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='USER_ENTERED',
        body={'values': values},
    ).execute()
