from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from purchase_order.views import  PurchaseOrderViewSet


router = DefaultRouter()
router.register('purchase_order', PurchaseOrderViewSet, basename='purchase-order-viewset')
urlpatterns = [
     path("api/",include(router.urls)),
]