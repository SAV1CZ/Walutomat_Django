from django.db import models



class AvaiableCurrencies(models.Model):
    Code = models.CharField(max_length=3, unique=True)
    Walutomat_Balance = models.DecimalField(max_digits=15, decimal_places=4, default=0)

    def __str__(self):
        return self.Code


class LocationsCurrencies(models.Model):
    Location = models.CharField(max_length=30, unique=True)
    Currency_Code = models.ForeignKey(AvaiableCurrencies, on_delete=models.PROTECT)

    def __str__(self):
        return self.Location


class Person(models.Model):
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)
    Email = models.EmailField(unique=True, null=False)
    Location = models.ForeignKey(LocationsCurrencies, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.Email} {self.Location}"


class Wallet(models.Model):
    Owner = models.ForeignKey(Person , on_delete=models.PROTECT)
    Currency = models.ForeignKey(AvaiableCurrencies, on_delete=models.PROTECT)
    Balance = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    Active = models.BooleanField(default=True)

    def __str__(self):
        return f"Owner: {self.Owner} : {self.Balance}{self.Currency}"

class CrossRate(models.Model):
    Base_Currency = models.ForeignKey(AvaiableCurrencies, on_delete=models.PROTECT, related_name="base_rates")
    Quote_Currency = models.ForeignKey(AvaiableCurrencies, on_delete=models.PROTECT, related_name="quote_rates")
    Exchange_Rate = models.DecimalField(max_digits=15, decimal_places=9)
    Updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.Base_Currency}/{self.Quote_Currency} = {self.Exchange_Rate}"

    
class Transaction(models.Model):
    Source = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="outcoming")
    Destination = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="incoming")
    Amount = models.DecimalField(max_digits=12, decimal_places=2)
    Base_Currency = models.ForeignKey(AvaiableCurrencies, on_delete=models.PROTECT)
    Time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Time}: {self.Amount}{self.Base_Currency}"