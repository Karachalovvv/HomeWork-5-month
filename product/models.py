from django.db import models

class Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'products')

    def __str__(self):
        return self.title

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'reviews')
    text = models.TextField()
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    def __str__(self):
        return f"{self.stars}★ - {self.text[:30]}"
    