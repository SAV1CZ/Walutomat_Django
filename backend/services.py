from decimal import Decimal, ROUND_FLOOR
from django.db import transaction
from backend.models import Wallet, CrossRate, AvaiableCurrencies, Transaction

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
 
    pair = CrossRate.objects.filter(
        Base_Currency__Code=base_code, 
        Quote_Currency__Code=quote_code).first()
    
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
    
    Transaction.objects.create(
        Source=source_wallet,
        Destination=destination_wallet,
        Amount=amount,
        Base_Currency=base_currency_obj)