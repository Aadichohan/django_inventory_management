from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store_product.views import  StoreProductViewSet


router = DefaultRouter()
router.register('store_product', StoreProductViewSet, basename='store-product-viewset')
urlpatterns = [
     path("api/",include(router.urls)),
]