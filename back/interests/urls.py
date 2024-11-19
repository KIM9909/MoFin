from django.urls import path
from . import views


urlpatterns = [
    path('save_deposit_products/', views.save_deposit_products, name='save_deposit_products'),
    path('deposit_product_options/', views.deposit_product_options, name='deposit_product_options'),
    path('top_rate/', views.top_rate, name='top_rate'),
]
