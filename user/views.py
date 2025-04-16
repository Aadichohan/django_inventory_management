from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from user.models import User
from user.userSerializer import UserSerializer
from django_inventory_management.response import DrfResponse


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'register':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                name=serializer.validated_data['name'],
                password=request.data.get('password'),
                role_id=serializer.validated_data['role_id']
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
            user = serializer.save(created_by=request.user)
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

    def destroy(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save(updated_by=request.user)
        return DrfResponse(
            data=[],
            status=status.HTTP_204_NO_CONTENT,
            response={"response": "User deleted successfully"},
            error={},
            headers={}
        ).to_json()
