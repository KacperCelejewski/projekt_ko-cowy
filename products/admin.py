from django.contrib import admin
from .models import Product, Category


# Rejestracja modelu Category w panelu admina
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")  # Wyświetlanie nazw kategorii i slugów
    search_fields = ("name",)  # Możliwość wyszukiwania po nazwie kategorii
    prepopulated_fields = {
        "slug": ("name",)
    }  # Automatyczne generowanie slug-u na podstawie nazwy


# Rejestracja modelu Product w panelu admina
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "available",
        "created",
        "updated",
    )
    list_filter = ("category", "available")  # Filtruj po kategorii i dostępności
    search_fields = ("name", "description")  # Wyszukiwanie po nazwie i opisie
