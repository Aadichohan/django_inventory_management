
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from role.models import Role
from role.roleSerializer import RoleSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        role = Role.objects.all()
        role_serializer = RoleSerializer(role, many=True)
        # print('role_serializer: ',role_serializer)
        return DrfResponse(
            data    = role_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        role_serializer = self.get_serializer(data=request.data)
        if role_serializer.is_valid():
            user = self.request.user
            role_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [role_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'role created successfully'},
                headers = {}
            ).to_json()
        # print(role_serializer.errors)
        return DrfResponse( 
            data    = [role_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [role_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        role = self.get_object()
        role_serializer = self.get_serializer(role)
        return DrfResponse(
            data    = [role_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        role = self.get_object()
        role_serializer = self.get_serializer(role, data= request.data)
        user = self.request.user
        if role_serializer.is_valid():
            role_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [role_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'role updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [role_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [role_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        role = self.get_object()
        role_serializer = self.get_serializer(role, data= request.data, partial=True)
        if role_serializer.is_valid():
            role_serializer.save()

            return DrfResponse( 
                data    = [role_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'role updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [role_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [role_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        role = self.get_object()
        # role.delete()
        role_serializer = self.get_serializer(role, data= request.data)
        user = self.request.user
        if role_serializer.is_valid():
            role_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 0)
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'role deleted successfully'},
            headers = {}
        ).to_json()
