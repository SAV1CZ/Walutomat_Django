from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExchangeInputSerializer,WalletSerializer
from .services import exchange 
from .models import Wallet


class ExchangeAPI(APIView):
    
    def post(self, request):
        
        serializer = ExchangeInputSerializer(data=request.data)
        
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        from_wallet_id = serializer.validated_data['from_wallet_id']
        source_currency = Wallet.objects.get(id=from_wallet_id)
        base_currency = source_currency.Currency
        to_wallet_id = serializer.validated_data['to_wallet_id']
        destination_currency = Wallet.objects.get(id=to_wallet_id)
        quote_currency = destination_currency.Currency
        amount = serializer.validated_data['amount']
        
       
        try:
            exchange(source_wallet_id=from_wallet_id, base_code=base_currency,destination_wallet_id=to_wallet_id, quote_code=quote_currency,amount_of_base=amount)

            return Response({"message": "Wymiana zakończona sukcesem","status": "SUCCESS"},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AllWalletsAPI(APIView):

    def get(self, request):

        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
