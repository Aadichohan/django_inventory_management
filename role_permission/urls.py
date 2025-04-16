from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from role.views import  RoleViewSet

router = DefaultRouter()
router.register('role_permission', RoleViewSet, basename='role-permission-viewset')
urlpatterns = [
     path("api/",include(router.urls)),
]