from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customer.views import  CustomerSerializer


router = DefaultRouter()
router.register('customer', CustomerSerializer, basename='customer-viewset')
urlpatterns = [
     path("api/",include(router.urls)),
]