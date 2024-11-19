from django.urls import path
from .views import ExchangeRateAPIView

urlpatterns = [
    path('api/exchange-rate/', ExchangeRateAPIView.as_view(), name='exchange-rate'),
]
