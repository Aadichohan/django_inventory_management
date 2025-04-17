
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from customer.models import Customer
from customer.customerSerializer import CustomerSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission

class StoreViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        customer = Customer.objects.all()
        customer_serializer = CustomerSerializer(customer, many=True)
        print(customer_serializer)
        return DrfResponse(
            data    = customer_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        customer_serializer = self.get_serializer(data=request.data)
        if customer_serializer.is_valid():
            user = self.request.user
            customer_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [customer_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'customer created successfully'},
                headers = {}
            ).to_json()
        # print(customer_serializer.errors)
        return DrfResponse( 
            data    = [customer_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [customer_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        customer = self.get_object()
        customer_serializer = self.get_serializer(customer)
        return DrfResponse(
            data    = [customer_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        customer = self.get_object()
        customer_serializer = self.get_serializer(customer, data= request.data)
        user = self.request.user
        if customer_serializer.is_valid():
            customer_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [customer_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'customer updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [customer_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [customer_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        customer = self.get_object()
        customer_serializer = self.get_serializer(customer, data= request.data, partial=True)
        if customer_serializer.is_valid():
            customer_serializer.save()

            return DrfResponse( 
                data    = [customer_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'customer updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [customer_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [customer_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        customer = self.get_object()
        # customer.delete()
        customer_serializer = self.get_serializer(customer, data= request.data)
        user = self.request.user
        if customer_serializer.is_valid():
            customer_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 0)
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'customer deleted successfully'},
            headers = {}
        ).to_json()
