from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from savings.models import DepositProducts

class SignupView(RegisterView):
    serializer_class = CustomRegisterSerializer
