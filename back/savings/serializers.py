from rest_framework import serializers
from .models import SavingsProducts, SavingsOptions

class SavingsProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsProducts
        fields = '__all__'


class SavingsOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsOptions
        fields = '__all__'
        read_only_fields = ('product', )
