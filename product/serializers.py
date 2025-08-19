from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Название категории не может быть пустым.")
        if len(value) < 2:
            raise serializers.ValidationError("Минимум 2 символа.")
        qs = Category.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Категория с таким названием уже существует.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Название товара не может быть пустым.")
        if len(value) < 2:
            raise serializers.ValidationError("Минимум 2 символа.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0.")
        return value

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Указанная категория не существует.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

    def validate_text(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Текст отзыва не может быть пустым.")
        if len(value) < 5:
            raise serializers.ValidationError("Минимум 5 символов.")
        return value

    def validate_stars(self, value):
        if not (1 <= value <= 5):
             raise serializers.ValidationError("Рейтинг (stars) должен быть от 1 до 5.")
        return value

    def validate_product(self, value):
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Указанный товар не существует.")
        return value


class ReviewShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewShortSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def get_rating(self, obj):
        if hasattr(obj, 'rating') and obj.rating is not None:
            return round(float(obj.rating), 2)
        avg = obj.reviews.aggregate(r=Avg('stars'))['r']
        return round(float(avg), 2) if avg is not None else 0.0