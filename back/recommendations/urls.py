from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('get-recommendations/', views.get_recommendations, name='get_recommendations'),
    path('finance-status/', views.get_personal_finance_status, name='finance_status'),
]