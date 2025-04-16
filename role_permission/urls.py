from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from role_permission.views import  RolePermissionViewSet

router = DefaultRouter()
router.register('role_permission', RolePermissionViewSet, basename='role-permission-viewset')
urlpatterns = [
     path("api/",include(router.urls)),
]