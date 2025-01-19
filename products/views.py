from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .serializers import ReviewSerializer


# --- Widok kategorii ---
class CategoryListView(ListAPIView):
    """
    Endpoint: Pobieranie wszystkich kategorii.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveAPIView):
    """
    Endpoint: Pobieranie pojedynczej kategorii po slug-u.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


# --- Widoki produktów ---
class ProductListView(ListAPIView):
    """
    Endpoint: Pobieranie wszystkich produktów z opcjonalnym filtrowaniem po kategorii
    oraz wyszukiwaniem po nazwie.
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        category_slug = self.request.query_params.get("category")
        search_query = self.request.query_params.get("search")

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset


class ProductDetailView(RetrieveAPIView):
    """
    Endpoint: Pobieranie szczegółów pojedynczego produktu po slug-u.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"


@api_view(["PATCH"])
def edit_review(request, slug, review_id):
    """
    Endpoint: Edycja opinii o produkcie.
    """
    product = get_object_or_404(Product, slug=slug)
    user = request.user

    if not user.is_authenticated:
        return Response(
            {"detail": "Musisz być zalogowany, aby edytować opinię."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    review = get_object_or_404(product.reviews, id=review_id)

    if user != review.user:
        return Response(
            {"detail": "Nie masz uprawnień do edycji tej opinii."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Pobierz dane z żądania
    data = request.data
    serializer = ReviewSerializer(instance=review, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail": "Opinia została zaktualizowana."},
            status=status.HTTP_200_OK,
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
def add_product_review(request, slug):
    """
    Endpoint: Dodanie opinii o produkcie.
    """
    product = get_object_or_404(Product, slug=slug)
    user = request.user

    if not user.is_authenticated:
        return Response(
            {"detail": "Musisz być zalogowany, aby dodać opinię."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Pobierz dane z żądania
    rating = request.data.get("rating")
    comment = request.data.get("comment")

    if not rating or not comment:
        return Response(
            {"detail": "Wszystkie pola są wymagane."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Tworzenie opinii
    review = product.reviews.create(user=user, rating=rating, comment=comment)
    return Response(
        {"detail": "Opinia została dodana.", "review_id": review.id},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def update_product(request, slug):
    """
    Endpoint: Aktualizacja produktu.
    """
    product = get_object_or_404(Product, slug=slug)
    user = request.user

    if not user.is_authenticated:
        return Response(
            {"detail": "Musisz być zalogowany, aby edytować produkt."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if user != product.user:
        return Response(
            {"detail": "Nie masz uprawnień do edycji tego produktu."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Pobierz dane z żądania
    data = request.data
    serializer = ProductSerializer(instance=product, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail": "Produkt został zaktualizowany."},
            status=status.HTTP_200_OK,
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["DELETE"])
def delete_product(request, slug):
    """
    Endpoint: Usunięcie produktu.
    """
    product = get_object_or_404(Product, slug=slug)
    user = request.user

    if not user.is_authenticated:
        return Response(
            {"detail": "Musisz być zalogowany, aby usunąć produkt."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if user != product.user:
        return Response(
            {"detail": "Nie masz uprawnień do usunięcia tego produktu."},
            status=status.HTTP_403_FORBIDDEN,
        )

    product.delete()
    return Response(
        {"detail": "Produkt został usunięty."},
        status=status.HTTP_204_NO_CONTENT,
    )


@api_view(["GET"])
def get_user_products(request):
    """
    Endpoint: Pobieranie produktów użytkownika.
    """
    user = request.user
    products = Product.objects.filter(user=user)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_prduct(request, slug):
    """
    Endpoint: Pobieranie produktu.
    """
    product = get_object_or_404(Product, slug=slug)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
