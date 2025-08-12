from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название категории не может быть пустым.")
        if len(value) < 2:
            raise serializers.ValidationError("Название категории должно содержать минимум 2 символа.")
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Категория с таким названием уже существует.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название товара не может быть пустым.")
        if len(value) < 2:
            raise serializers.ValidationError("Название товара должно содержать минимум 2 символа.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0.")
        return value

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Выбранная категория не существует.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Текст отзыва не может быть пустым.")
        if len(value) < 5:
            raise serializers.ValidationError("Отзыв должен содержать минимум 5 символов.")
        return value

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value

    def validate_product(self, value):
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Выбранный товар не существует.")
        return value
from rest_framework import serializers
from .models import Category, Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review