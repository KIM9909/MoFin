from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(
        required=False,
        max_length=255
    )
    birth = serializers.DateField(
        required=False,
    )
    preference = serializers.CharField(
        required=False,
        max_length=255
    )

    def get_cleaned_data(self):
        cleaned_data = {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'preference': self.validated_data.get('preference', ''),
        }
        
        birth = self.validated_data.get('birth', None)
        if birth:
            cleaned_data['birth'] = str(birth)

        return cleaned_data
