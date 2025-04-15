from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import  StoreViewSet


router = DefaultRouter()
router.register('store', StoreViewSet, basename='store-viewset')
urlpatterns = [
     path("api/",include(router.urls)),
]