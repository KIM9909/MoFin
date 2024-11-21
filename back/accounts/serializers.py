from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from savings.models import SavingsProducts

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=False, max_length=255)
    birth = serializers.DateField(required=False)
    preference = serializers.CharField(required=False, max_length=255)
    # subscribe_deposits = serializers.

    def get_cleaned_data(self):
        cleaned_data = {
            'nickname': self.validated_data.get('nickname', ''),
            'birth': self.validated_data.get('birth', ''),
            'preference': self.validated_data.get('preference', ''),

        }
        
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        
        return user