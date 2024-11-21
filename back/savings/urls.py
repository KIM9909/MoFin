from django.urls import path
from . import views


urlpatterns = [
    path('save_deposit_products/', views.save_deposit_products, name='save_deposit_products'),
    path('deposit_products/', views.deposit_products, name='deposit_products'),
    path('deposit_product_options/<str:fin_prdt_cd>/', views.deposit_product_options, name='deposit_product_options'),
    path('deposit_product_details/<str:fin_prdt_cd>/', views.deposit_product_details, name="deposit_product_details"),
    path('save_savings_products/', views.save_savings_products, name='save_savings_products'),
    path('savings_products/', views.savings_products, name="savings_products"),
    path('savings_product_options/<str:fin_prdt_cd>/', views.savings_product_options, name='savings_product_options'),
    path('savings_product_details/<str:fin_prdt_cd>/', views.savings_product_details, name="savings_product_details"),
    path('subscribe/<str:product_type>/<str:fin_prdt_cd>/', views.toggle_subscription, name='toggle_subscription'),
    path('subscriptions/', views.get_subscriptions, name='get_subscriptions'),

]
