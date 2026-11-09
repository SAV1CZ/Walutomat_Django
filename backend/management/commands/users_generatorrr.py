from django.core.management.base import BaseCommand
from backend.models import AvaiableCurrencies, LocationsCurrencies, Person , Wallet
from faker import Faker
import random


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
        
            allowed_location_objects = {l.Location: l for l in LocationsCurrencies.objects.all()}
            currency_objects = {c.Code: c for c in AvaiableCurrencies.objects.all()}
            
            LOCATION_PROPABILITY = [10,6,2,3,1,4,5,6,4,1,2,6,5,9,5,12,4,5,10]
            countries_list = list(allowed_location_objects.keys())
            currencies_list = list(currency_objects.keys())
            CURRENCIES_PROPABILITY = [7,29,20,8,10,2,3,11,6,4]
            generated_emails = set() 
            persons_to_create = []
            wallets_to_create = []
            Y_N = ["Y", "N"]
            Y_N_WEIGHTS = [15,85]

            num_users = 5000
            fake = Faker()

            for _ in range(num_users):
                first_name = fake.first_name()
                last_name = fake.last_name()
                    
                email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@test.com"
                while email in generated_emails:
                    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1000, 9999)}@test.com"
                generated_emails.add(email)

                country = random.choices(countries_list, weights=LOCATION_PROPABILITY, k=1)[0]
                location = allowed_location_objects[country]
                persons_to_create.append(Person(First_Name=first_name, Last_Name=last_name, Email=email, Location=location))

            if persons_to_create:
                Person.objects.bulk_create(persons_to_create)
                for person in persons_to_create:

                    available_currencies = list(currency_objects.keys())
                    user_weights = list(CURRENCIES_PROPABILITY)
                    
                    user_currencies = []
                    user_location = person.Location
                    base_currency_code = user_location.Currency_Code.Code
                    base_currency = currency_objects[base_currency_code]
                    
                    balance = round(random.uniform(50.0,30000.0),2)
                    wallets_to_create.append(Wallet(Owner=person, Currency=base_currency, Balance=balance))

                    
                    index = available_currencies.index(base_currency_code)
                    available_currencies.pop(index)
                    user_weights.pop(index)
                    user_currencies.append(base_currency_code)

                   
                    second_currency = random.choices(available_currencies, weights=user_weights, k=1)[0]
                    currency = currency_objects[second_currency]
                    wallets_to_create.append(Wallet(Owner=person, Currency=currency, Balance=0))

                    index = available_currencies.index(second_currency)
                    available_currencies.pop(index)
                    user_weights.pop(index)
                    user_currencies.append(second_currency)

                  
                    third_account = random.choices(Y_N, weights=Y_N_WEIGHTS, k=1)[0]

                    if third_account == "Y":
                        third_currency = random.choices(available_currencies, weights=user_weights, k=1)[0]
                        currency = currency_objects[third_currency]
                        wallets_to_create.append(Wallet(Owner=person, Currency=currency, Balance=0))

            if wallets_to_create:
                Wallet.objects.bulk_create(wallets_to_create)

        except Exception as e:
            import traceback
            traceback.print_exc()