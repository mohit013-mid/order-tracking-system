from rest_framework import serializers
from .models import Product
 
 
class ProductSerializer(serializers.ModelSerializer):
 
    image = serializers.ImageField(required=True)
    stock = serializers.IntegerField(required=False, default=0)
 
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "image", "stock", "created_at"]
        read_only_fields = ["id", "created_at"]