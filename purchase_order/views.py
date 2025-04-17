
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from purchase_order.models import PurchaseOrder
from purchase_order.purchaseOrderSerializer import PurchaseOrderSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission

class PurchaseOrderViewSet(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        purchase_order = PurchaseOrder.objects.all()
        purchase_order_serializer = PurchaseOrderSerializer(purchase_order, many=True)
        print(purchase_order_serializer)
        return DrfResponse(
            data    = purchase_order_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        purchase_order_serializer = self.get_serializer(data=request.data)
        if purchase_order_serializer.is_valid():
            user = self.request.user
            purchase_order_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [purchase_order_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'purchase_order created successfully'},
                headers = {}
            ).to_json()
        # print(purchase_order_serializer.errors)
        return DrfResponse( 
            data    = [purchase_order_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [purchase_order_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order_serializer = self.get_serializer(purchase_order)
        return DrfResponse(
            data    = [purchase_order_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order_serializer = self.get_serializer(purchase_order, data= request.data)
        user = self.request.user
        if purchase_order_serializer.is_valid():
            purchase_order_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [purchase_order_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'purchase_order updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [purchase_order_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [purchase_order_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order_serializer = self.get_serializer(purchase_order, data= request.data, partial=True)
        if purchase_order_serializer.is_valid():
            purchase_order_serializer.save()

            return DrfResponse( 
                data    = [purchase_order_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'purchase_order updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [purchase_order_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [purchase_order_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        purchase_order = self.get_object()
        # purchase_order.delete()
        purchase_order_serializer = self.get_serializer(purchase_order, data= request.data)
        user = self.request.user
        if purchase_order_serializer.is_valid():
            purchase_order_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 0)
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'purchase_order deleted successfully'},
            headers = {}
        ).to_json()
