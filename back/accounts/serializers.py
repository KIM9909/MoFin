from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from savings.models import SavingsProducts, DepositProducts
from django.contrib.auth.password_validation import validate_password


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)
    birth = serializers.DateField(required=False, allow_null=True)
    preference = serializers.CharField(required=False, allow_null=True)
    annual_income = serializers.IntegerField(required=False, allow_null=True)
    total_assets = serializers.IntegerField(required=False, allow_null=True)
    profile_img = serializers.ImageField(required=False, allow_null=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'nickname': self.validated_data.get('nickname', ''),
            'birth': self.validated_data.get('birth', None),
            'preference': self.validated_data.get('preference', None),
            'annual_income': self.validated_data.get('annual_income', None),
            'total_assets': self.validated_data.get('total_assets', None),
            'profile_img': self.validated_data.get('profile_img', None),

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
    profile_img = serializers.ImageField(required=False, allow_null=True)
    profile_img_url = serializers.SerializerMethodField()
    
    def get_profile_img_url(self, obj):
        if obj.profile_img:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_img.url)
            return obj.profile_img.url
        return None

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + (
            'nickname', 'birth', 'preference', 
            'subscribe_deposits', 'subscribe_savings',
            'annual_income', 'total_assets',
            'profile_img', 'profile_img_url'
        )
        read_only_fields = ('email',)


User = get_user_model()

class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    nickname = serializers.CharField(required=False)
    birth = serializers.DateField(required=False, allow_null=True)
    preference = serializers.CharField(required=False, allow_null=True)
    annual_income = serializers.IntegerField(required=False, allow_null=True)
    total_assets = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'nickname', 'birth', 'preference', 'annual_income', 'total_assets')

    def validate(self, attrs):
        user = self.context['request'].user
        
        # 현재 사용자의 email과 동일하다면 유일성 검사를 건너뜀
        if attrs.get('email') == user.email:
            attrs.pop('email', None)
            
        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance