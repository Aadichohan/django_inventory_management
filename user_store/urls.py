from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_store.views import  UserStoreViewSet


router = DefaultRouter()
router.register('user_store', UserStoreViewSet, basename='user-store-viewset')
urlpatterns = [
     path("api/",include(router.urls)),
]