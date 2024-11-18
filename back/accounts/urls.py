from django.urls import path
from .views import SignupView

urlpatterns = [
    path('accounts/signup/', SignupView.as_view(), name='signup'),
]
