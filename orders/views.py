from rest_framework import generics
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


# Widok listy i tworzenia zamówień
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# Widok szczegółów zamówienia
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# Widok listy i tworzenia pozycji zamówienia
class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


# Widok szczegółów pozycji zamówienia
class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


# Widok listy i tworzenia płatności
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


# Widok szczegółów płatności
class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


@api_view(["DELETE"])
def delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
def update_order(request, id):
    order = get_object_or_404(Order, id=id)
    serializer = OrderSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_order_item(request, id):
    order_item = get_object_or_404(OrderItem, id=id)
    order_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
def update_order_item(request, id):
    order_item = get_object_or_404(OrderItem, id=id)
    serializer = OrderItemSerializer(order_item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_payment(request, id):
    payment = get_object_or_404(Payment, id=id)
    payment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
def update_payment(request, id):
    payment = get_object_or_404(Payment, id=id)
    serializer = PaymentSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD)
