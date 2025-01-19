# products/urls.py
from django.urls import path
from .views import CategoryListView, CategoryDetailView

urlpatterns = [
    # Kategorię lista
    path("categories/", CategoryListView.as_view(), name="category-list"),
    # Kategoria szczegóły (po slug)
    path(
        "categories/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"
    ),
]
