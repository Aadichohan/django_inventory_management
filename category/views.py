
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from category.models import Category
from category.categorySerializer import CategorySerializer
from django_inventory_management.response import DrfResponse


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        category = Category.objects.all()
        category_serializer = CategorySerializer(category, many=True)
        return DrfResponse(
            data    = category_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        category_serializer = self.get_serializer(data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return DrfResponse( 
                data    = [category_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'category created successfully'},
                headers = {}
            ).to_json()
        # print(category_serializer.errors)
        return DrfResponse( 
            data    = [category_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [category_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        category = self.get_object()
        category_serializer = self.get_serializer(category)
        return DrfResponse(
            data    = [category_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        category = self.get_object()
        category_serializer = self.get_serializer(category, data= request.data)
        if category_serializer.is_valid():
            category_serializer.save()

            return DrfResponse( 
                data    = [category_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'category updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [category_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [category_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        category = self.get_object()
        category_serializer = self.get_serializer(category, data= request.data, partial=True)
        if category_serializer.is_valid():
            category_serializer.save()

            return DrfResponse( 
                data    = [category_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'category updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [category_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [category_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        category = self.get_object()
        category.delete()
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'category deleted successfully'},
            headers = {}
        ).to_json()
    
    # Custom action for marking a category as favorite (example)
    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        category = self.get_object()
        category.desc = 'favorite'
        category.save()
        return Response({'status': 'category marked as favorite'})