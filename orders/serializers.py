from rest_framework import serializers
from .models import Order, OrderItem, Payment


# Serializer dla zamówienia
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


# Serializer dla pozycji zamówienia
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


# Serializer dla płatności
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
