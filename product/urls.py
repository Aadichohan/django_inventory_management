from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import  ProductViewSet


router = DefaultRouter()
router.register('product', ProductViewSet, basename='product-viewset')
urlpatterns = [
     path("api/",include(router.urls)),
]