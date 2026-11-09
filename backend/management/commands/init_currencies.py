from django.core.management.base import BaseCommand
from backend.models import AvaiableCurrencies, CrossRate
import requests

class Command(BaseCommand):

    def handle(self, *args, **options):

        CURRENCIES = ["PLN", "USD", "EUR", "GBP", "CHF", "BRL", "JPY", "HKD", "DKK", "SEK"]

        try:
            existing_currencies = set(AvaiableCurrencies.objects.values_list('Code', flat=True))            
            new_currencies_objects = [AvaiableCurrencies(Code=code) for code in CURRENCIES if code not in existing_currencies]
            if new_currencies_objects:
                AvaiableCurrencies.objects.bulk_create(new_currencies_objects)
        
            all_pairs_to_add = []
            
            for base_currency in CURRENCIES:
                url = f"https://api.frankfurter.app/latest?from={base_currency}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    rates = response.json().get("rates", {})
                    for target_currency, exchange_rate in rates.items():
                        if target_currency in CURRENCIES:
                            all_pairs_to_add.append({
                                "Base_Currency": base_currency,
                                "Quote_Currency": target_currency,
                                "Exchange_Rate": exchange_rate})
                else:
                    raise Exception(f"{base_currency} not in api")

            currency_objects = {c.Code: c for c in AvaiableCurrencies.objects.all()}
            existing_pairs = set(CrossRate.objects.values_list('Base_Currency', 'Quote_Currency'))
            new_pairs_objects = []

            for pair in all_pairs_to_add:
                base_code = pair["Base_Currency"]
                quote_code = pair["Quote_Currency"]

                if (base_code, quote_code) not in existing_pairs:
                    base_instance = currency_objects.get(base_code)
                    quote_instance = currency_objects.get(quote_code)

                    if base_instance and quote_instance:    
                        new_pairs_objects.append(
                            CrossRate(
                            Base_Currency=base_instance,    
                            Quote_Currency=quote_instance,  
                            Exchange_Rate=pair["Exchange_Rate"]))
                        
            if new_pairs_objects:
                CrossRate.objects.bulk_create(new_pairs_objects)

        except Exception as e:
            import traceback
            traceback.print_exc()
           
