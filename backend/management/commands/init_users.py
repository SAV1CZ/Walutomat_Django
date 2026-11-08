from django.core.management.base import BaseCommand
from backend.models import AvaiableCurrencies, Person, Wallet, LocationsCurrencies

class Command(BaseCommand):

    def handle(self, *args, **options):

        LOCATIONS = [{"Poland":"PLN"},{"Ukraine":"EUR"},{"Lithuania":"EUR"},{"Estonia":"EUR"},{"Latvia":"EUR"},{"Sweden":"SEK"},
        {"Denmark":"DKK"},{"Germany":"EUR"},{"France":"EUR"},{"Netherland":"EUR"},{"Spain":"EUR"},{"Switzerland":"CHF"},{"UK":"GBP"},
        {"Brazil":"BRL"},{"Mexico":"USD"},{"USA":"USD"},{"Argentina":"USD"},{"Japan":"JPY"},{"Hongkong":"HKD"}]

        LOCATION_PROPABILITY = [10,6,2,3,1,4,5,6,4,1,2,6,5,9,5,12,4,5,10]


        existing_locations = set(LocationsCurrencies.objects.values_list("Location", flat=True))
        new_locations = [LocationsCurrencies]