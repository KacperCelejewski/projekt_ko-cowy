from django.urls import path
from .views import CreateCheckoutSessionView, PaymentSuccessView, PaymentCancelView
from .views import stripe_webhook

urlpatterns = [
    path(
        "create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create_checkout_session",
    ),
    path("payments/success/", PaymentSuccessView.as_view(), name="payment_success"),
    path("payments/cancel/", PaymentCancelView.as_view(), name="payment_cancel"),
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
]
