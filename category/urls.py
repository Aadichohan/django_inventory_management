from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from class_based_django_rest_framework.Views.Book.BookView import  BookView
# from class_based_django_rest_framework.Views.Book.BookViewSet import  BookViewSet
# from e_commerce.ModelViews.User import User

# from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
# router.register('books-viewset-rest', BookViewSet, basename='books-viewset-rest')
urlpatterns = [
    #  path('books-view-rest/', view=BookView.as_view(), name='book-list'),
    #  path('books-view-rest/<int:book_id>/', BookView.as_view(), name='book-detail'),
    #  path("",include(router.urls)),
    #  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]