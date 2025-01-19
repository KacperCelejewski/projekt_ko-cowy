import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from orders.models import Cart, OrderItem
from django.views.decorators.csrf import csrf_exempt

# Inicjalizacja Stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class PaymentSuccessView(APIView):
    def get(self, request):
        return JsonResponse({"message": "Payment was successful"})


class PaymentCancelView(APIView):
    def get(self, request):
        return JsonResponse({"message": "Payment was cancelled"})


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Pobierz koszyk użytkownika
            cart = Cart.objects.get(user=request.user)
            order_items = OrderItem.objects.filter(cart=cart)

            # Stwórz listę produktów
            line_items = []
            for item in order_items:
                line_items.append(
                    {
                        "price_data": {
                            "currency": "pln",
                            "product_data": {
                                "name": item.product.name,
                            },
                            "unit_amount": int(item.product.price * 100),
                        },
                        "quantity": item.quantity,
                    }
                )

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=settings.STRIPE_CANCEL_URL,
            )
            return JsonResponse({"sessionId": session["id"]})
        except Cart.DoesNotExist:
            return JsonResponse({"detail": "Cart not found"}, status=404)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)


# views.py


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

        # Obsłuż zdarzenia Stripe, np. PaymentIntent.succeeded
        if event["type"] == "payment_intent.succeeded":
            payment_intent = event["data"]["object"]
            # Wykonaj akcję po pomyślnej płatności, np. zmień status zamówienia

        return JsonResponse({"status": "success"}, status=200)
    except ValueError as e:
        # Błąd w przetwarzaniu ładunku
        return JsonResponse({"status": "failure"}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Błąd w weryfikacji sygnatury
        return JsonResponse({"status": "failure"}, status=400)
