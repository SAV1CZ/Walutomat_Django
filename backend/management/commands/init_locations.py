from backend.models import AvaiableCurrencies, LocationsCurrencies
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):

        try:
            LOCATIONS = [{"Poland":"PLN"},{"Ukraine":"EUR"},{"Lithuania":"EUR"},{"Estonia":"EUR"},{"Latvia":"EUR"},{"Sweden":"SEK"},
            {"Denmark":"DKK"},{"Germany":"EUR"},{"France":"EUR"},{"Netherland":"EUR"},{"Spain":"EUR"},{"Switzerland":"CHF"},{"UK":"GBP"},
            {"Brazil":"BRL"},{"Mexico":"USD"},{"USA":"USD"},{"Argentina":"USD"},{"Japan":"JPY"},{"Hongkong":"HKD"}]

            existing_locations = set(LocationsCurrencies.objects.values_list("Location", flat=True))
            currencies_objects = {c.Code:c for c in AvaiableCurrencies.objects.all()}
            new_locations_objects = []

            for pair in LOCATIONS:
                name , code = list(pair.items())[0]
                if name in existing_locations:
                    continue
                if code in currencies_objects:
                    currency_instance = currencies_objects[code]
                    new_locations_objects.append(LocationsCurrencies(Location=name, Currency_Code=currency_instance))
            if new_locations_objects:
                LocationsCurrencies.objects.bulk_create(new_locations_objects)        
        except Exception:
            import traceback
            traceback.print_exc()

    