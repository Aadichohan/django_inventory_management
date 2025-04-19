
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from endpoint_master.models import EndpointMaster
from endpoint_master.endpoint_master_serializer import EndpointMasterSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission


class EndpointMasterViewSet(ModelViewSet):
    queryset = EndpointMaster.objects.all()
    serializer_class = EndpointMasterSerializer
    permission_classes = []
    
    def list(self, request):
        endpoint = EndpointMaster.objects.all()
        endpoint_serializer = EndpointMasterSerializer(endpoint, many=True)
        # print('endpoint_serializer: ',endpoint_serializer)
        return DrfResponse(
            data    = endpoint_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        endpoint_serializer = self.get_serializer(data=request.data)
        if endpoint_serializer.is_valid():
            user = self.request.user
            endpoint_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [endpoint_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'endpoint created successfully'},
                headers = {}
            ).to_json()
        # print(endpoint_serializer.errors)
        return DrfResponse( 
            data    = [endpoint_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [endpoint_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        endpoint = self.get_object()
        endpoint_serializer = self.get_serializer(endpoint)
        return DrfResponse(
            data    = [endpoint_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        endpoint = self.get_object()
        endpoint_serializer = self.get_serializer(endpoint, data= request.data)
        user = self.request.user
        if endpoint_serializer.is_valid():
            endpoint_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [endpoint_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'endpoint updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [endpoint_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [endpoint_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        endpoint = self.get_object()
        endpoint_serializer = self.get_serializer(endpoint, data= request.data, partial=True)
        if endpoint_serializer.is_valid():
            endpoint_serializer.save()

            return DrfResponse( 
                data    = [endpoint_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'endpoint updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [endpoint_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [endpoint_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        endpoint = self.get_object()
        # endpoint.delete()
        endpoint_serializer = self.get_serializer(endpoint, data= request.data)
        user = self.request.user
        if endpoint_serializer.is_valid():
            endpoint_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 0)
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'endpoint deleted successfully'},
            headers = {}
        ).to_json()
