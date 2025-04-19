from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from role_permission.models import RolePermission
from role_permission.rolePermissionSerializer import RolePermissionSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission


class RolePermissionViewSet(ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def list(self, request):
        role_id = request.query_params.get('role_id', None)

        if role_id:
            role_permission = RolePermission.objects.filter(role_id=role_id)
        else:
            role_permission = RolePermission.objects.all()

        serializer = self.get_serializer(role_permission, many=True)
        return DrfResponse(
            data=serializer.data,
            status=status.HTTP_200_OK,
            error={},
            headers={}
        ).to_json()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return DrfResponse(
                data=[serializer.data],
                status=status.HTTP_201_CREATED,
                error={},
                response={'response': 'role_permission created successfully'},
                headers={}
            ).to_json()

        return DrfResponse(
            data=[serializer.data],
            status=status.HTTP_400_BAD_REQUEST,
            error=[serializer.errors],
            response={'response': 'Something went wrong'},
            headers={}
        ).to_json()

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DrfResponse(
            data=[serializer.data],
            status=status.HTTP_200_OK,
            error={},
            headers={}
        ).to_json()

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=self.request.user, updated_at=datetime.utcnow())
            return DrfResponse(
                data=[serializer.data],
                status=status.HTTP_200_OK,
                error={},
                response={'response': 'role_permission updated successfully'},
                headers={}
            ).to_json()

        return DrfResponse(
            data=[serializer.data],
            status=status.HTTP_400_BAD_REQUEST,
            error=[serializer.errors],
            response={'response': 'Something went wrong'},
            headers={}
        ).to_json()

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=self.request.user, updated_at=datetime.utcnow())
            return DrfResponse(
                data=[serializer.data],
                status=status.HTTP_200_OK,
                error={},
                response={'response': 'role_permission updated successfully'},
                headers={}
            ).to_json()

        return DrfResponse(
            data=[serializer.data],
            status=status.HTTP_400_BAD_REQUEST,
            error=[serializer.errors],
            response={'response': 'Something went wrong'},
            headers={}
        ).to_json()

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.is_active = 0
        instance.updated_by = self.request.user
        instance.updated_at = datetime.utcnow()
        instance.save()

        return DrfResponse(
            status=status.HTTP_204_NO_CONTENT,
            error={},
            response={'response': 'role_permission deleted successfully'},
            headers={}
        ).to_json()