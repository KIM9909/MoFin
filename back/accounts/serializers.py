from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from savings.models import SavingsProducts

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
    joined_products = serializers.ListField(
        child=serializers.IntegerField(),  # product_id 리스트로 받기
        required=False,
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

        joined_products = self.validated_data.get('joined_products', [])
        if joined_products:
            cleaned_data['joined_products'] = joined_products

        return cleaned_data

    def save(self, request):
        user = super().save(request)
        
        # 가입한 상품 정보 처리
        joined_products = self.validated_data.get('joined_products', [])
        if joined_products:
            products = SavingsProducts.objects.filter(id__in=joined_products)
            user.joined_products.set(products)  # 사용자의 joined_products 필드에 해당 상품들 추가
        
        return user