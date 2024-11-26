from django.urls import path
from .views import UserDeleteView
from . import views

urlpatterns = [
    path('delete/', UserDeleteView.as_view(), name='account_delete'),
    path('update/', views.update_user, name='user-update'),

]
