#
# IMPORTS
#
# Python std library
import datetime as dt
from json.decoder import JSONDecodeError

# Django
from django.db import models

# Project
from config.models import Category, ContractType, Fee, PaymentForm
from store import store
from trello import add_label_to_card, get_card, remove_card_label

# Typing
from typing import Tuple


#
# CODE
#
def get_choices(field: str) -> Tuple[Tuple[str, str]]:
    """
    Get the available choices for a field.
    """
    try:

        # setup the field to model searcher
        FIELD_TO_MODEL = {
            'activities': Activity,
            'categories': Category,
            'contracts': ContractType,
            'fees': Fee,
            'payment-forms': PaymentForm,
        }

        # get the names of the choices
        name_list = [obj.name for obj in FIELD_TO_MODEL[field].objects.all()]

        # return tuple of choices
        return tuple((name, name) for name in name_list)

    # any error: return empty tuple
    except Exception as e:
        print(e)
        return ()


class Prospector(models.Model):
    """
    A prospector is any person in contact with a company.
    """

    # prospector information
    name = models.CharField(max_length=100)
    email = models.EmailField()

    # prospector types
    is_seller = models.BooleanField(default=False)
    is_contractor = models.BooleanField(default=False)
    is_postseller = models.BooleanField(default=False)

    # trello lists ids
    list_id_sales = models.CharField(max_length=100, blank=True, null=True)
    list_id_contracts = models.CharField(max_length=100, blank=True, null=True)

    @property
    def has_delays(self) -> bool:
        """
        Check if any company of this prospector has delays.
        """
        return any(
            map(
                lambda c: c.needs_reminder,
                Company.objects.filter(prospector=self)
            )
        )

    @property
    def contact_count(self) -> int:
        """
        Get the number of companies that this prospector is in contact with.
        """
        return Company.objects.filter(prospector=self).count()

    @property
    def contact_list(self) -> list:
        """
        Get the list of companies that this prospector is in contact with.
        """
        return list(Company.objects.filter(prospector=self))

    @property
    def closed_count(self) -> int:
        """
        Get the number of companies that this prospector closed contracts with.
        """
        return Company.objects.filter(prospector=self,
                                      stage=store['closed']).count()

    def __str__(self) -> str:
        return self.name


class Company(models.Model):
    """
    Company model.
    """

    # company information
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100,
                                choices=get_choices('categories'),
                                blank=True)
    main_contact = models.EmailField(blank=True)

    # trello card id
    card_id = models.CharField(max_length=100)

    # prospection information
    prospector = models.ForeignKey(Prospector,
                                   on_delete=models.SET_NULL,
                                   limit_choices_to={'is_seller': True},
                                   related_name='companies',
                                   related_query_name='company',
                                   null=True)
    stage = models.CharField(max_length=100,
                             choices=get_choices('stages'),
                             default=store['stages']['initial'])
    last_activity = models.DateField(default=dt.date.today)
    comments_number = models.PositiveSmallIntegerField(default=0)

    @property
    def inactive_time(self) -> dt.timedelta:
        """
        Get the time that the contact with this company has been inactive.
        """
        return dt.date.today() - self.last_activity

    @property
    def needs_reminder(self) -> bool:
        """
        See if this company prospector needs a reminder.
        """
        return not (
            (self.inactive_time.days < store['deadlines']['urgent'])
            or (self.stage in store['stages']['no-reminder'])
        )

    @property
    def status_label(self) -> str:
        """
        Get the label corresponding to this company contact status.
        """
        # is inactive for less time than attention deadline: return updated
        if self.inactive_time.days < store['deadlines']['attention']:
            return 'updated'

        # is inactive for less time than urgent deadline: return attention
        if self.inactive_time.days < store['deadlines']['urgent']:
            return 'attention'

        # is inactive for more time than urgent deadline: return urgent
        return 'urgent'

    def turn_updated(self) -> None:
        """
        Turn this company updated.
        """
        self.last_activity = dt.date.today()
        self.save()

    def check_update(self) -> None:
        """
        Check if this company had any activity and update its stage.
        """
        # get prospection progress graph
        progress_graph = store['stages']['graph']

        # current stage is not terminal: check update
        if self.stage in progress_graph.keys():

            # get company card
            try:
                card = get_card(self.card_id).json()

            # could not get company card: abort
            except JSONDecodeError:
                print(f'{self.name} não presente no quadro!')
                return

            # get card labels
            labels = card['labels']

            # initialize stage label checker
            has_stage_label = False

            # check if any of the labels are of a new stage
            for label in labels:

                # found stage label: check for update
                if label['name'] in store['labels']['stage-list']:

                    # is valid following stage: update stage
                    if label['name'] in progress_graph[self.stage]:
                        self.turn_updated()
                        self.stage = label['name']
                        self.save()

                    # update stage label checker
                    has_stage_label = True

            # remove any label prior to the current state
            for label in labels:
                if label['name'] in store['labels']['stage-list'] \
                   and label['name'] != self.stage:
                    remove_card_label(self.card_id, label['id'])

            # no stage label: post initial
            if not has_stage_label:
                add_label_to_card(self.card_id,
                                  store['labels']['initial']['id'])

            # card has a new comment: update
            if card['badges']['comments'] > self.comments_number:
                self.turn_updated()
                self.comments_number = card['badges']['comments']
                self.save()

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self) -> str:
        return self.name


class Activity(models.Model):
    """
    Activity model.
    """

    # activity information
    name = models.CharField(max_length=100, unique=True)

    # prospection information
    prospector = models.ForeignKey(Prospector,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)

    class Meta:
        verbose_name_plural = 'activities'

    def __str__(self) -> str:
        return self.name


class Contract(models.Model):
    """
    Contract model.
    """

    # company reference
    company = models.OneToOneField(Company,
                                   on_delete=models.CASCADE)

    # trello card id
    card_id = models.CharField(max_length=100)

    # prospection information
    contractor = models.ForeignKey(Prospector,
                                   on_delete=models.SET_NULL,
                                   limit_choices_to={'is_contractor': True},
                                   related_name='contractor_contracts',
                                   related_query_name='contractor_contract',
                                   null=True,
                                   blank=True)
    postseller = models.ForeignKey(Prospector,
                                   on_delete=models.SET_NULL,
                                   limit_choices_to={'is_postseller': True},
                                   related_name='posteller_contracts',
                                   related_query_name='posteller_contract',
                                   null=True,
                                   blank=True)
    date_closed = models.DateField(default=dt.date.today)

    # payment information
    intake = models.PositiveIntegerField(default=0)
    payday = models.DateField(blank=True, null=True)
    contract_type = models.CharField(
        max_length=100,
        choices=get_choices('contracts')
    )
    fee_type = models.CharField(max_length=100,
                                choices=get_choices('fees'))
    payment_form = models.CharField(
        max_length=100,
        choices=get_choices('payment-forms'),
        blank=True
    )
    needs_receipt = models.BooleanField(default=False)

    # exposition information
    stand_size = models.PositiveSmallIntegerField(blank=True, null=True)
    stand_pos = models.CharField(max_length=100, blank=True, null=True)
    custom_stand = models.BooleanField(default=False)
    activities = models.ManyToManyField(Activity)

    # misc
    observations = models.TextField(blank=True)

    def __str__(self) -> str:
        if self.company.name.endswith('s'):
            return f'{self.company.name}\' contract'
        return f'{self.company.name}\'s contract'
