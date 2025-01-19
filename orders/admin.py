from django.contrib import admin
from .models import Order, OrderItem, Discount, Payment, Cart


# Rejestracja Discount w panelu admina
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("code", "percentage", "active", "expires_at")


# Rejestracja Cart w panelu admina
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")


# Rejestracja Order w panelu admina
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "total_price",
        "created_at",
        "updated_at",
    )
    list_filter = ("status",)
    search_fields = ("user__username",)


# Rejestracja OrderItem w panelu admina
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
    search_fields = ("product__name",)


# Rejestracja Payment w panelu admina
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "amount", "status", "payment_date")
    list_filter = ("status",)
