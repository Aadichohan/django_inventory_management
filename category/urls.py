from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from class_based_django_rest_framework.Views.Book.BookView import  BookView
from category.views import  CategoryViewSet
# from e_commerce.ModelViews.User import User

# from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category-viewset')
urlpatterns = [
    #  path('books-view-rest/', view=BookView.as_view(), name='book-list'),
    #  path('books-view-rest/<int:book_id>/', BookView.as_view(), name='book-detail'),
     path("api/",include(router.urls)),
    #  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]