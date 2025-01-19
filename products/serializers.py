from rest_framework import serializers
from .models import Product, Category, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    category = (
        CategorySerializer()
    )  # Możesz także użyć ID kategorii zamiast pełnych danych

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "description",
            "price",
            "stock",
            "available",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
