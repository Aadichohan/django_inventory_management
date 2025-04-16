
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from product.models import Product
from product.productSerializer import ProductSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    
    def list(self, request):
        product = Product.objects.all()
        product_serializer = ProductSerializer(product, many=True)
        print(product_serializer)
        return DrfResponse(
            data    = product_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        product_serializer = self.get_serializer(data=request.data)
        if product_serializer.is_valid():
            user = self.request.user
            print(user)
            product_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [product_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'product created successfully'},
                headers = {}
            ).to_json()
        # print(product_serializer.errors)
        return DrfResponse( 
            data    = [product_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [product_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        product = self.get_object()
        product_serializer = self.get_serializer(product)
        return DrfResponse(
            data    = [product_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        product = self.get_object()
        product_serializer = self.get_serializer(product, data= request.data)
        user = self.request.user
        if product_serializer.is_valid():
            product_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [product_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'product updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [product_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [product_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        product = self.get_object()
        product_serializer = self.get_serializer(product, data= request.data, partial=True)
        if product_serializer.is_valid():
            product_serializer.save()

            return DrfResponse( 
                data    = [product_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'product updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [product_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [product_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        product = self.get_object()
        # product.delete()
        product_serializer = self.get_serializer(product, data= request.data)
        user = self.request.user
        # if product_serializer.is_valid():
        print('stop')
        product_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 1)
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'product deleted successfully'},
            headers = {}
        ).to_json()
    