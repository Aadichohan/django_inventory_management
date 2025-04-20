
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from supplier.models import Supplier
from supplier.supplierSerializer import SupplierSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission

class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        supplier = Supplier.objects.all()
        supplier_serializer = SupplierSerializer(supplier, many=True)
        print(supplier_serializer)
        return DrfResponse(
            data    = supplier_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        supplier_serializer = self.get_serializer(data=request.data)
        if supplier_serializer.is_valid():
            user = self.request.user
            supplier_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [supplier_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'supplier created successfully'},
                headers = {}
            ).to_json()
        # print(supplier_serializer.errors)
        return DrfResponse( 
            data    = [supplier_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [supplier_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        supplier = self.get_object()
        supplier_serializer = self.get_serializer(supplier)
        return DrfResponse(
            data    = [supplier_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        supplier = self.get_object()
        supplier_serializer = self.get_serializer(supplier, data= request.data)
        user = self.request.user
        if supplier_serializer.is_valid():
            supplier_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [supplier_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'supplier updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [supplier_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [supplier_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        supplier = self.get_object()
        supplier_serializer = self.get_serializer(supplier, data= request.data, partial=True)
        if supplier_serializer.is_valid():
            supplier_serializer.save()

            return DrfResponse( 
                data    = [supplier_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'supplier updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [supplier_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [supplier_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        supplier = self.get_object()
        user = self.request.user
        # supplier.delete()
        data = {
            "is_active": 0,
            "updated_by": user.pk,
            "updated_at": datetime.utcnow()
        }
        supplier_serializer = self.get_serializer(supplier, data= request.data, partial = True)
        if supplier_serializer.is_valid():
            supplier_serializer.save()
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'supplier deleted successfully'},
            headers = {}
        ).to_json()
