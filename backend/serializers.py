from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from services import register_new_user
from decimal import Decimal
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'Owner', 'Currency', 'Balance']
        read_only_fields = ['id', 'Owner', 'Currency', 'Balance']



@extend_schema_field({
    'type': 'string',
    'format': 'decimal',
    'example': '0.00'})
class AmountField(serializers.DecimalField):
    pass



class RegisterPerson(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    location = serializers.CharField()
    second_currency = serializers.CharField()

    def create(self, validated_data):
        return register_new_user(validated_data)

class UserActionSerializer(serializers.Serializer):
    to_wallet_id = serializers.IntegerField()
    amount = AmountField(max_digits=12, decimal_places=2,min_value=Decimal('0.01'))

class ExchangeInputSerializer(serializers.Serializer):
    from_wallet_id = serializers.IntegerField()
    to_wallet_id = serializers.IntegerField()

    amount = AmountField(max_digits=12, decimal_places=2,min_value=Decimal('0.01'))


class DepositSerializer(serializers.Serializer):
    
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Kwota wpłaty musi być większa od zera.")
        return value