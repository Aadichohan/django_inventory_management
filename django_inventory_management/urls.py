"""
URL configuration for django_inventory_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/', include('category.urls')),
    path('product/', include('product.urls')),
    path('store/', include('store.urls')),
    path('store_product/', include('store_product.urls')),
    path('user/', include('user.urls')),
    path('user_store/', include('user_store.urls')),
    path('role/', include('role.urls')),
    path('role_permission/', include('role_permission.urls')),
    path('customer/', include('customer.urls')),
    path('supplier/', include('supplier.urls')),
    path('purchase_order/', include('purchase_order.urls')),
    path('sales_order/', include('sales_order.urls')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
