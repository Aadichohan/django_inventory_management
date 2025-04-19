from django.urls import path, include
from rest_framework.routers import DefaultRouter
from endpoint_master.views import EndpointMasterViewSet

router = DefaultRouter()
router.register('endpoint', EndpointMasterViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]