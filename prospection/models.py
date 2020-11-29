#
# IMPORTS
#
# Python std library
import datetime as dt

# Django
from django.db import models

# Project
from utils import get_choices_from_store, get_store


#
# CODE
#
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
    list_id_sales = models.CharField(max_length=100, null=True)
    list_id_contracts = models.CharField(max_length=100, null=True)

    @property
    def has_delays(self) -> bool:
        """
        Check if any company of this prospector has delays.
        """
        for c in Company.objects.filter(prospector=self):
            if c.needs_reminder:
                return True
        return False

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
                                      stage=get_store()['closed']).count()

    def __str__(self) -> str:
        return self.name


class Company(models.Model):
    """
    Company model.
    """

    # company information
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100,
                                choices=get_choices_from_store('categories'),
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
                             choices=get_choices_from_store('stages'),
                             default=get_store()['stages']['initial'])
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
            (self.inactive_time.days < get_store()['deadlines']['urgent'])
            or (self.seller_stage in get_store()['stages']['no-reminder'])
        )

    @property
    def status_label(self) -> str:
        """
        Get the label corresponding to this company contact status.
        """
        # get configuration store
        store = get_store()

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

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self) -> str:
        return self.name
