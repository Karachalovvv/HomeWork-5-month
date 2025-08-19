"""
URL configuration for shop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from product import views as pviews

from users.views import RegisterView, ConfirmView, LoginView

urlpatterns = [
    path('api/v1/categories/', pviews.category_list_create_api_view),
    path('api/v1/categories/<int:id>/', pviews.category_detail_api_view),
    path('api/v1/products/', pviews.product_list_create_api_view),
    path('api/v1/products/<int:id>/', pviews.product_detail_api_view),
    path('api/v1/products/reviews/', pviews.products_with_reviews_api_view),
    path('api/v1/reviews/', pviews.review_list_create_api_view),
    path('api/v1/reviews/<int:id>/', pviews.review_detail_api_view),
    path('api/v1/users/register/', RegisterView.as_view()),
    path('api/v1/users/confirm/', ConfirmView.as_view()),
    path('api/v1/users/login/', LoginView.as_view()),
]

