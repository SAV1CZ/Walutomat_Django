from django.db import models



class AvaiableCurrencies(models.Model):
    code = models.CharField(max_length=3, unique=True)
    walutomat_balance = models.DecimalField(max_digits=15, decimal_places=4)

    def __str__(self):
        return self.code


class LocationsCurrencies(models.Model):
    location = models.CharField(max_length=30, unique=True)
    currency_code = models.ForeignKey(AvaiableCurrencies, on_delete=models.PROTECT)

    def __str__(self):
        return self.location


class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True, null=False)
    location = models.ForeignKey(LocationsCurrencies, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.email} {self.location}"


class Wallet(models.Model):
    owner = models.ForeignKey(Person , on_delete=models.PROTECT)
    currency = models.ForeignKey(AvaiableCurrencies, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=10,decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Owner: {self.owner} : {self.balance}{self.currency}"

class CrossRate(models.Model):
    base_currency = models.ForeignKey(AvaiableCurrencies, on_delete=models.PROTECT, related_name="base_rates")
    quote_currency = models.ForeignKey(AvaiableCurrencies, on_delete=models.PROTECT, related_name="quote_rates")
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=9)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.base_currency}/{self.quote_currency} = {self.exchange_rate}"

    
class Transaction(models.Model):
    source = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="outcoming")
    destination = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="incoming")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    base_currency = models.ForeignKey(AvaiableCurrencies, on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.time}: {self.amount}{self.base_currency}"