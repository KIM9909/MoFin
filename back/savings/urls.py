from django.urls import path
from . import views


urlpatterns = [
    path('save_savings_products/', views.save_savings_products, name='save_savings_products'),
    path('savings_product_options/<str:fin_prdt_cd>/', views.savings_product_options, name='savings_product_options'),
    path('savings_product_details/<str:fin_prdt_cd>/', views.savings_product_details, name="savings_product_details")
]
