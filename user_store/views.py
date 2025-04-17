
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from user_store.models import UserStore
from user_store.userstoreSerializer import UserStoreSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission

class UserStoreViewSet(ModelViewSet):
    queryset = UserStore.objects.all()
    serializer_class = UserStoreSerializer
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        user_store = UserStore.objects.all()
        user_store_serializer = UserStoreSerializer(user_store, many=True)
        print(user_store_serializer)
        return DrfResponse(
            data    = user_store_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        user_store_serializer = self.get_serializer(data=request.data)
        if user_store_serializer.is_valid():
            user = self.request.user
            user_store_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [user_store_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'user_store created successfully'},
                headers = {}
            ).to_json()
        # print(user_store_serializer.errors)
        return DrfResponse( 
            data    = [user_store_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [user_store_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        user_store = self.get_object()
        user_store_serializer = self.get_serializer(user_store)
        return DrfResponse(
            data    = [user_store_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        user_store = self.get_object()
        user_store_serializer = self.get_serializer(user_store, data= request.data)
        user = self.request.user
        if user_store_serializer.is_valid():
            user_store_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [user_store_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'user_store updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [user_store_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [user_store_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        user_store = self.get_object()
        user_store_serializer = self.get_serializer(user_store, data= request.data, partial=True)
        if user_store_serializer.is_valid():
            user_store_serializer.save()

            return DrfResponse( 
                data    = [user_store_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'user_store updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [user_store_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [user_store_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        user_store = self.get_object()
        # user_store.delete()
        user_store_serializer = self.get_serializer(user_store, data= request.data)
        user = self.request.user
        if user_store_serializer.is_valid():
            user_store_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 0)
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'user_store deleted successfully'},
            headers = {}
        ).to_json()
