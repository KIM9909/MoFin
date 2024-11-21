from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User
from savings.models import SavingsProducts, DepositProducts

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)
    birth = serializers.DateField(required=False, allow_null=True)
    preference = serializers.CharField(required=False, allow_null=True)
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'nickname': self.validated_data.get('nickname', ''),
            'birth': self.validated_data.get('birth', None),
            'preference': self.validated_data.get('preference', None),
        })
        return data

class CustomUserDetailsSerializer(UserDetailsSerializer):
    subscribe_deposits = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DepositProducts.objects.all(),
        required=False
    )
    subscribe_savings = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SavingsProducts.objects.all(),
        required=False
    )

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + (
            'nickname', 'birth', 'preference', 
            'subscribe_deposits', 'subscribe_savings'
        )
        read_only_fields = ('email',)