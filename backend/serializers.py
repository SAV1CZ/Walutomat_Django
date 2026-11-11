from rest_framework import serializers
from decimal import Decimal
from .models import Wallet



class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'Owner', 'Currency', 'Balance']
        read_only_fields = ['id', 'Owner','Currency', 'Balance'] #chroni przed zmienianiem tych pol przez użytkownika


class ExchangeInputSerializer(serializers.Serializer):
    
    from_wallet_id = serializers.IntegerField()
    to_wallet_id = serializers.IntegerField()

    amount = serializers.DecimalField(
        max_digits=12, 
        decimal_places=2,
        min_value=Decimal('0.01'),)