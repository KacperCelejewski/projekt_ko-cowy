from django.urls import path
from . import views

urlpatterns = [
    # Endpointy do zamówień
    path("orders/", views.OrderListCreateView.as_view(), name="order-list-create"),
    path("orders/<int:id>/", views.OrderDetailView.as_view(), name="order-detail"),
    # Endpointy do pozycji zamówienia
    path(
        "order-items/",
        views.OrderItemListCreateView.as_view(),
        name="order-item-list-create",
    ),
    path(
        "order-items/<int:id>/",
        views.OrderItemDetailView.as_view(),
        name="order-item-detail",
    ),
    # Endpoint do płatności
    path(
        "payments/", views.PaymentListCreateView.as_view(), name="payment-list-create"
    ),
    path(
        "payments/<int:id>/", views.PaymentDetailView.as_view(), name="payment-detail"
    ),
]
