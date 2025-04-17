
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from sales_order.models import SalesOrder
from sales_order.salesOrderSerializer import SalesOrderSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission

class SalesOrderViewSet(ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        sales_order = SalesOrder.objects.all()
        sales_order_serializer = SalesOrderSerializer(sales_order, many=True)
        print(sales_order_serializer)
        return DrfResponse(
            data    = sales_order_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        sales_order_serializer = self.get_serializer(data=request.data)
        if sales_order_serializer.is_valid():
            user = self.request.user
            sales_order_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [sales_order_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'sales_order created successfully'},
                headers = {}
            ).to_json()
        # print(sales_order_serializer.errors)
        return DrfResponse( 
            data    = [sales_order_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [sales_order_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        sales_order = self.get_object()
        sales_order_serializer = self.get_serializer(sales_order)
        return DrfResponse(
            data    = [sales_order_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        sales_order = self.get_object()
        sales_order_serializer = self.get_serializer(sales_order, data= request.data)
        user = self.request.user
        if sales_order_serializer.is_valid():
            sales_order_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [sales_order_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'sales_order updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [sales_order_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [sales_order_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        sales_order = self.get_object()
        sales_order_serializer = self.get_serializer(sales_order, data= request.data, partial=True)
        if sales_order_serializer.is_valid():
            sales_order_serializer.save()

            return DrfResponse( 
                data    = [sales_order_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'sales_order updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [sales_order_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [sales_order_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        sales_order = self.get_object()
        # sales_order.delete()
        sales_order_serializer = self.get_serializer(sales_order, data= request.data)
        user = self.request.user
        if sales_order_serializer.is_valid():
            sales_order_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 0)
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'sales_order deleted successfully'},
            headers = {}
        ).to_json()
