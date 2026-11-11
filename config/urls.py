from backend.views import AllWalletsAPI, ExchangeAPI
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wallets/',AllWalletsAPI.as_view(),name='wallets-list'),
    path('exchange/',ExchangeAPI.as_view(),name='exchange-action'),]
