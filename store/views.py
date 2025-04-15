
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from store.models import Store
from store.storeSerializer import StoreSerializer
from django_inventory_management.response import DrfResponse


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = []
    
    def list(self, request):
        store = Store.objects.all()
        store_serializer = StoreSerializer(store, many=True)
        print(store_serializer)
        return DrfResponse(
            data    = store_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        store_serializer = self.get_serializer(data=request.data)
        if store_serializer.is_valid():
            user = self.request.user
            store_serializer.save(created_by=user)
            return DrfResponse( 
                data    = [store_serializer.data], 
                status  = status.HTTP_201_CREATED, 
                error   = {}, 
                response = {'response': 'store created successfully'},
                headers = {}
            ).to_json()
        # print(store_serializer.errors)
        return DrfResponse( 
            data    = [store_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [store_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()
        

    def retrieve(self, request, pk=None):
        store = self.get_object()
        store_serializer = self.get_serializer(store)
        return DrfResponse(
            data    = [store_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        store = self.get_object()
        store_serializer = self.get_serializer(store, data= request.data)
        user = self.request.user
        if store_serializer.is_valid():
            store_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [store_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'store updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [store_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [store_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        store = self.get_object()
        store_serializer = self.get_serializer(store, data= request.data, partial=True)
        if store_serializer.is_valid():
            store_serializer.save()

            return DrfResponse( 
                data    = [store_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'store updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [store_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [store_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        store = self.get_object()
        # store.delete()
        store_serializer = self.get_serializer(store, data= request.data)
        user = self.request.user
        if store_serializer.is_valid():
            store_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 0)
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'store deleted successfully'},
            headers = {}
        ).to_json()
