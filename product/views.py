from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    CategoryWithCountSerializer,
    ProductSerializer,
    ProductDetailSerializer,
    ReviewSerializer,
    ProductReviewSerializer,
)

@api_view(["GET"])
def category_list_api_view(request):
    categories = Category.objects.annotate(products_count=Count("products"))
    serializer = CategoryWithCountSerializer(categories, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=404)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

@api_view(["GET"])
def product_list_api_view(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)

@api_view(["GET"])
def review_list_api_view(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=404)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(["GET"])
def product_reviews_list_api_view(request):
    products = Product.objects.prefetch_related("reviews").all()
    result = []

    for product in products:
        reviews = product.reviews.all()
        rating = reviews.aggregate(avg=Avg("stars"))["avg"] or 0
        serializer = ProductReviewSerializer(product, context={"rating": rating})
        result.append({
            "id": product.id,
            "title": product.title,
            "reviews": ReviewSerializer(reviews, many=True).data,
            "rating": round(rating, 2)
        })

    average_rating = Review.objects.aggregate(avg=Avg("stars"))["avg"] or 0
    return Response({
        "average_rating": round(average_rating, 2),
        "products": result
    })
