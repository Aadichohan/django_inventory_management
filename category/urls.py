from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from category.views import  CategoryViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category-viewset')
urlpatterns = [
    #  path('books-view-rest/', view=BookView.as_view(), name='book-list'),
    #  path('books-view-rest/<int:book_id>/', BookView.as_view(), name='book-detail'),
     path("api/",include(router.urls)),
    #  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]