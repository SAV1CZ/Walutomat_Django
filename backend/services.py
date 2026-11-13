from backend.models import Wallet, CrossRate, AvaiableCurrencies, Transaction, Person, LocationsCurrencies
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_FLOOR
from django.db import transaction


@transaction.atomic
def exchange(base_code, quote_code, amount_of_base, source_wallet_id, destination_wallet_id):


    margin = Decimal("0.997") 
    amount = Decimal(str(amount_of_base))
    
   
    source_wallet = Wallet.objects.select_for_update().filter(
        id=source_wallet_id, 
        Currency__Code=base_code).first()
    
    if not source_wallet:
        raise ValueError(f"Wallet source ID {source_wallet_id} for {base_code} not found.")
    if source_wallet.Balance < amount:
        raise ValueError("Not enough money to complete operation.")
        
   
    destination_wallet = Wallet.objects.select_for_update().filter(
        id=destination_wallet_id, 
        Currency__Code=quote_code).first()
    
    if not destination_wallet:
        raise ValueError(f"Wallet destination ID {destination_wallet_id} for {quote_code} not found.")
 
    pair = CrossRate.objects.filter(Base_Currency__Code=base_code, Quote_Currency__Code=quote_code).first()
    
    if not pair:
        raise ValueError(f"Exchange rate for {base_code} -> {quote_code} not available.")
        
    ratio = pair.Exchange_Rate
    clients_part = amount * ratio * margin
    client_receive = clients_part.quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
    real = amount * ratio
    profit = real - client_receive
    
   
    source_wallet.Balance -= amount
    source_wallet.save()
    
    destination_wallet.Balance += client_receive
    destination_wallet.save()
    
    
    walutomat_currency = AvaiableCurrencies.objects.filter(Code=quote_code).first()
    if walutomat_currency and hasattr(walutomat_currency, 'Walutomat_Balance'):
        walutomat_currency.Walutomat_Balance += profit
        walutomat_currency.save()
        

    base_currency_obj = AvaiableCurrencies.objects.filter(Code=base_code).first()
    
    transaction_detail = Transaction.objects.create(Source=source_wallet,Destination=destination_wallet,Amount=amount,Base_Currency=base_currency_obj)
    
    return transaction_detail



@transaction.atomic
def transfer_funds(source_wallet_id, destination_wallet_id, amount_of_money, owner):


    amount = Decimal(str(amount_of_money)) 
    source_wallet = Wallet.objects.select_for_update().filter(id=source_wallet_id, Owner=owner).first()
    
    if not source_wallet:
        raise ValueError("Source wallet not found or access denied.")
    
    if source_wallet.Balance < amount:
        raise ValueError("Not enough money to complete operation.")
        
   
    destination_wallet = Wallet.objects.select_for_update().filter(id=destination_wallet_id).first()
    
    if not destination_wallet:
        raise ValueError("Destination wallet not found.")
        
  
    if source_wallet.Currency != destination_wallet.Currency:
        raise ValueError("Currencies must match for direct transfer. Use exchange endpoint.")
        
  
    source_wallet.Balance -= amount
    source_wallet.save()
    
    destination_wallet.Balance += amount
    destination_wallet.save()
    
   
    transaction_detail = Transaction.objects.create(Source=source_wallet,Destination=destination_wallet,Amount=amount,Base_Currency=source_wallet.Currency)
    
    return transaction_detail



@transaction.atomic
def register_new_user(validated_data):

    user = User.objects.create_user(
        username=validated_data['email'],
        email=validated_data['email'],
        password=validated_data['password'])

    loc_currency_obj = LocationsCurrencies.objects.get(Location=validated_data['location'])
    second_currency_obj = AvaiableCurrencies.objects.get(Code=validated_data['second_currency'])

    person = Person.objects.create(
        User_Obj=user,
        First_Name=validated_data['first_name'],
        Last_Name=validated_data['last_name'],
        Email=validated_data['email'],
        Location=loc_currency_obj)

    Wallet.objects.create(Owner=person,Currency=loc_currency_obj.Currency_Code,Balance=0.00)
    Wallet.objects.create(Owner=person,Currency=second_currency_obj,Balance=0.00)

    return user





@transaction.atomic
def deposit_to_base_wallet(user, amount):
    person = Person.objects.get(User_Obj=user)
    loc_currency = LocationsCurrencies.objects.get(Location=person.Location)
    
    wallet = Wallet.objects.select_for_update().get(Owner=person,Currency=loc_currency.Currency_Code)
    
    wallet.Balance += Decimal(str(amount))
    wallet.save()
    return wallet
