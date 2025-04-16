
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from role_permission.models import RolePermission
from role_permission.rolePermissionSerializer import RolePermissionSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission

class RolePermissionViewSet(ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        role_id = request.query_params.get('role_id', None)

        if role_id:
            role_permission = RolePermission.objects.filter(role_id=role_id)
        else:
             role_permission = RolePermission.objects.all()
        # role_permission = RolePermission.objects.all()
        role_permission_serializer = RolePermissionSerializer(role_permission, many=True)
        # print('role_permission_serializer list: ',role_permission_serializer)
        return DrfResponse(
            data    = role_permission_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        role_permission_serializer = self.get_serializer(data=request.data)
        # print('RolePermissionViewSet request.data ',request.data)
        # print('role_permission_serializer ', role_permission_serializer)
        if role_permission_serializer.is_valid():
            user = self.request.user
            role_permission_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [role_permission_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'role_permission created successfully'},
                headers = {}
            ).to_json()
        # print(role_permission_serializer.errors)
        return DrfResponse( 
            data    = [role_permission_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [role_permission_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        role_permission = self.get_object()
        role_permission_serializer = self.get_serializer(role_permission)
        return DrfResponse(
            data    = [role_permission_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        role_permission = self.get_object()
        role_permission_serializer = self.get_serializer(role_permission, data= request.data)
        user = self.request.user
        if role_permission_serializer.is_valid():
            role_permission_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [role_permission_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'role_permission updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [role_permission_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [role_permission_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        role_permission = self.get_object()
        role_permission_serializer = self.get_serializer(role_permission, data= request.data, partial=True)
        if role_permission_serializer.is_valid():
            role_permission_serializer.save()

            return DrfResponse( 
                data    = [role_permission_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'role_permission updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [role_permission_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [role_permission_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        role_permission = self.get_object()
        # role_permission.delete()
        role_permission_serializer = self.get_serializer(role_permission, data= request.data)
        user = self.request.user
        if role_permission_serializer.is_valid():
            role_permission_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 0)
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'role_permission deleted successfully'},
            headers = {}
        ).to_json()
