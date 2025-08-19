from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'reviews')
    text = models.TextField()
    stars = models.PositiveSmallIntegerField(default=5)  
    
    def __str__(self):
        return f"{self.stars}★ for {self.product}"
    