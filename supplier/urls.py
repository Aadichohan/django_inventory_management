from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from supplier.views import  SupplierViewSet


router = DefaultRouter()
router.register('supplier', SupplierViewSet, basename='supplier-viewset')
urlpatterns = [
     path("api/",include(router.urls)),
]