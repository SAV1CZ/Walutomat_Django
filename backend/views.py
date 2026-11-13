from .serializers import ExchangeInputSerializer,WalletSerializer,UserActionSerializer, RegisterPerson, DepositSerializer
from .services import exchange, transfer_funds, deposit_to_base_wallet
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet, Person
from rest_framework import status



class WalletListView(generics.ListAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Wallet.objects.filter(Owner=self.request.user.id)



class UserExchange(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=UserActionSerializer)
    def post(self, request, pk=None):

        person_obj = get_object_or_404(Person, User_Obj_id=request.user.id)
        source_wallet = get_object_or_404(Wallet, pk=pk, Owner=person_obj)
        
        
        serializer = UserActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        base_currency = source_wallet.Currency.Code
        to_wallet_id = serializer.validated_data['to_wallet_id']
        amount = serializer.validated_data['amount']
        
        destination_wallet = get_object_or_404(Wallet, id=to_wallet_id, Owner=person_obj)
        quote_currency = destination_wallet.Currency.Code
        
        
        try:
            exchange(
                source_wallet_id=source_wallet.id, 
                base_code=base_currency,
                destination_wallet_id=destination_wallet.id, 
                quote_code=quote_currency,
                amount_of_base=amount)

            return Response({
                "message": "Exchange transaction completed",
                "status": "SUCCESS"}, status=status.HTTP_200_OK)
        
        except ValueError as e:
          
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"DEBUG EXCEPTION: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 





class TransferAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=UserActionSerializer)
    def post(self, request, pk=None):

        person_obj = get_object_or_404(Person, User_Obj_id=request.user.id)
        source_wallet = get_object_or_404(Wallet, pk=pk, Owner=person_obj)
        
        
        serializer = UserActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        target_wallet_id = serializer.validated_data['to_wallet_id']
        amount = serializer.validated_data['amount']
        
        try:
            transfer_funds(
                source_wallet_id=source_wallet.id,
                destination_wallet_id=target_wallet_id,
                amount_of_money=amount,
                owner=person_obj)

            return Response({
                "message": "Transfer completed successfully",
                "status": "SUCCESS"}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"DEBUG EXCEPTION: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class Register(APIView):

    permission_classes = [permissions.AllowAny]
    @extend_schema(request=RegisterPerson,)

    def post(self, request):
        serializer = RegisterPerson(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class Deposit(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=DepositSerializer)
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            try:
                deposit_to_base_wallet(user=request.user,amount=serializer.validated_data['amount'])
                return Response(
                    {"message": "Operation successfull."}, 
                    status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)