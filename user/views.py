from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from datetime import datetime
from django.utils import timezone

from user.models import User
from user.userSerializer import UserSerializer
from user.ResetPasswordSerializer import ResetPasswordSerializer

from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'register':
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            is_staff = serializer.validated_data.get('is_staff', False)
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                name=serializer.validated_data['name'],
                password=request.data.get('password'),
                role_id=serializer.validated_data['role_id'],
                is_staff=is_staff
            )
            return DrfResponse(
                data=[UserSerializer(user).data],
                status=status.HTTP_201_CREATED,
                response={"response": "User registered successfully"},
                error={},
                headers={}
            ).to_json()

        return DrfResponse(
            data=[],
            status=status.HTTP_400_BAD_REQUEST,
            error=serializer.errors,
            response={"response": "User registration failed"},
            headers={}
        ).to_json()

    @action(detail=True, methods=['post'], url_path='reset-password')
    def reset_password(self, request, pk=None):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return DrfResponse(
                data=[],
                status=status.HTTP_404_NOT_FOUND,
                response={"response": "User not found"},
                error={"error": "Invalid user"},
                headers={}
            ).to_json()

        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return DrfResponse(
                data=[UserSerializer(user).data],
                status=status.HTTP_200_OK,
                response={"response": "Password reset successfully"},
                error={},
                headers={}
            ).to_json()

        return DrfResponse(
            data=[],
            status=status.HTTP_400_BAD_REQUEST,
            error=serializer.errors,
            response={"response": "Password reset failed"},
            headers={}
        ).to_json()
    

    def list(self, request):
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return DrfResponse(
            data=serializer.data,
            status=status.HTTP_200_OK,
            error={},
            headers={}
        ).to_json()

    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return DrfResponse(
            data=[serializer.data],
            status=status.HTTP_200_OK,
            error={},
            headers={}
        ).to_json()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password', None)

            user = serializer.save(created_by=request.user)

            if password:
                user.set_password(password)  # Hash the password
                user.save()
            return DrfResponse(
                data=[UserSerializer(user).data],
                status=status.HTTP_201_CREATED,
                response={"response": "User created successfully"},
                error={},
                headers={}
            ).to_json()
        return DrfResponse(
            data=[],
            status=status.HTTP_400_BAD_REQUEST,
            error=serializer.errors,
            response={"response": "User creation failed"},
            headers={}
        ).to_json()

    def update(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            
            serializer.save(updated_by=request.user)
            password = request.data.get('password', None)
            if password:
                user.set_password(password)  # Hash the password
                user.save()
            return DrfResponse(
                data=[serializer.data],
                status=status.HTTP_200_OK,
                response={"response": "User updated successfully"},
                error={},
                headers={}
            ).to_json()
        return DrfResponse(
            data=[],
            status=status.HTTP_400_BAD_REQUEST,
            error=serializer.errors,
            response={"response": "User update failed"},
            headers={}
        ).to_json()

    def partial_update(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return DrfResponse(
                data=[serializer.data],
                status=status.HTTP_200_OK,
                response={"response": "User partially updated successfully"},
                error={},
                headers={}
            ).to_json()
        return DrfResponse(
            data=[],
            status=status.HTTP_400_BAD_REQUEST,
            error=serializer.errors,
            response={"response": "Partial update failed"},
            headers={}
        ).to_json()

    # def destroy(self, request, pk=None):
    #     user = self.get_object()
    #     user.is_active = False
    #     user.save(updated_by=request.user, updated_at=timezone.now())
    #     return DrfResponse(
    #         data=[],
    #         status=status.HTTP_204_NO_CONTENT,
    #         response={"response": "User deleted successfully"},
    #         error={},
    #         headers={}
    #     ).to_json()

    # def destroy(self, request, pk=None):
    #     user = self.get_object()
    #     # purchase_order.delete()
    #     user_serializer = self.get_serializer(user, data= request.data)
    #     user = self.request.user
    #     if user_serializer.is_valid():
    #         user_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 0)
    #     return DrfResponse( 
         
    #         status  = status.HTTP_204_NO_CONTENT, 
    #         error   = {}, 
    #         response = {'response': 'user deleted successfully'},
    #         headers = {}
    #     ).to_json()


    def destroy(self, request, pk=None):
        user = self.get_object()  # get the object to delete
        current_user = request.user   # who is performing the delete

        # We are doing a partial update with soft delete flag
        serializer = self.get_serializer(user, data={
            "is_active": 0,
            "updated_by": current_user.pk,
            "updated_at": datetime.utcnow()
        }, partial=True)
        # print( {
        #     "is_active": 0,
        #     "updated_by": current_user.pk,
        #     "updated_at": datetime.utcnow()
        # })
        if serializer.is_valid():
            serializer.save()
            return DrfResponse(
                status=status.HTTP_204_NO_CONTENT,
                error={},
                response={'response': 'User deleted successfully'},
                headers={}
            ).to_json()
        else:
            return DrfResponse(
                status=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
                response={"response": "Invalid data while deleting"},
                headers={}
            ).to_json()
