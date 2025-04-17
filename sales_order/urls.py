from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sales_order.views import  SalesOrderViewSet


router = DefaultRouter()
router.register('sales_order', SalesOrderViewSet, basename='sales-order-viewset')
urlpatterns = [
     path("api/",include(router.urls)),
]