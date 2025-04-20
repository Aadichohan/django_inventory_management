
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from store_product.models import StoreProduct
from store_product.storeProductSerializer import StoreProductSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission

class StoreProductViewSet(ModelViewSet):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        store_product = StoreProduct.objects.all()
        store_product_serializer = StoreProductSerializer(store_product, many=True)
        print(store_product_serializer)
        return DrfResponse(
            data    = store_product_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        store_product_serializer = self.get_serializer(data=request.data)
        if store_product_serializer.is_valid():
            user = self.request.user
            store_product_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [store_product_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'store_product created successfully'},
                headers = {}
            ).to_json()
        # print(store_product_serializer.errors)
        return DrfResponse( 
            data    = [store_product_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [store_product_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        store_product = self.get_object()
        store_product_serializer = self.get_serializer(store_product)
        return DrfResponse(
            data    = [store_product_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        store_product = self.get_object()
        store_product_serializer = self.get_serializer(store_product, data= request.data)
        user = self.request.user
        if store_product_serializer.is_valid():
            store_product_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [store_product_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'store_product updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [store_product_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [store_product_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        store_product = self.get_object()
        store_product_serializer = self.get_serializer(store_product, data= request.data, partial=True)
        if store_product_serializer.is_valid():
            store_product_serializer.save()

            return DrfResponse( 
                data    = [store_product_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'store_product updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [store_product_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [store_product_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        store_product = self.get_object()
        user = self.request.user
        # store_product.delete()
        data = {
            "is_active": 0,
            "updated_by": user.pk,
            "updated_at": datetime.utcnow()
        }
        store_product_serializer = self.get_serializer(store_product, data= data, partial = True)
        if store_product_serializer.is_valid():
            store_product_serializer.save()
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'store_product deleted successfully'},
            headers = {}
        ).to_json()
