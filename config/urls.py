from backend.views import ExchangeAPI, WalletListView, UserExchange, TransferAPI, Register, Deposit
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/',SpectacularAPIView.as_view(),name='schema'),
    path('docs/',SpectacularSwaggerView.as_view(),name='Swagger'),
    path('Token/get/token/', TokenObtainPairView.as_view(), name='Token-Actions'),
    path('Token/refresh/', TokenRefreshView.as_view(), name='Token-Refresh'),
    path('User/wallets/list/', WalletListView.as_view(), name='User-Wallets'),
    path('User/wallets/<int:pk>/exchange/', UserExchange.as_view(), name='Internal-Exchange'),
    path('User/wallets/<int:pk>/transfer/', TransferAPI.as_view(), name='Transfer'),
    path('Register/',Register.as_view(), name='Register'),
    path('User/deposit/',Deposit.as_view(), name='Deposit')]


