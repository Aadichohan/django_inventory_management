
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from decimal import Decimal

from purchase_order.models import PurchaseOrder
from store_product.models import StoreProduct
from purchase_order.purchaseOrderSerializer import PurchaseOrderSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission

class PurchaseOrderViewSet(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        print('data: ',request.method)
        purchase_order = PurchaseOrder.objects.all()
        purchase_order_serializer = PurchaseOrderSerializer(purchase_order, many=True, context={'request': request})
        # print(purchase_order_serializer)
        return DrfResponse(
            data    = purchase_order_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def create(self, request):
        quantity =  Decimal(str(request.data.get('quantity', 0)))
        unit_price =  Decimal(str(request.data.get('unit_price', 0)))
        total_price = quantity * unit_price if quantity and unit_price else 0.00

        data = request.data.copy()
        data['total_price'] = total_price
        purchase_order_serializer = self.get_serializer(data=data, context={'request': request})
        if purchase_order_serializer.is_valid():
            user = request.user
            purchase_order = purchase_order_serializer.save(created_by=user)

            store = purchase_order.store
            product = purchase_order.product

            try:
                store_product = StoreProduct.objects.get(store=store, product=product)
                store_product.quantity += quantity
                store_product.purchase_price = unit_price
                store_product.sell_price = unit_price + (unit_price * Decimal('0.10'))
                store_product.updated_by = user
                store_product.updated_at = datetime.utcnow()
                print('purchase order store_product', store_product)
                store_product.save()

                # ✅ Return yahan add karo
                return DrfResponse(
                    data=[purchase_order_serializer.data],
                    status=status.HTTP_201_CREATED,
                    response={"response": "Purchase order created and existing store stock updated"},
                    error={}, headers={}
                ).to_json()

            except StoreProduct.DoesNotExist:
                StoreProduct.objects.create(
                    store=store,
                    product=product,
                    quantity=quantity,
                    purchase_price=unit_price,
                    sell_price=unit_price + (unit_price * Decimal('0.10')),
                    created_by=user
                )
                return DrfResponse(
                    data=[purchase_order_serializer.data],
                    status=status.HTTP_201_CREATED,
                    response={"response": "Purchase order created and new store stock added"},
                    error={}, headers={}
                ).to_json()

        else:
            print("Serializer Errors: ", purchase_order_serializer.errors)
            return DrfResponse(
                data=[],
                status=status.HTTP_400_BAD_REQUEST,
                error=[purchase_order_serializer.errors],
                response={"response": "Something went wrong"},
                headers={}
            ).to_json()

    # def create(self, request):
    #     purchase_order_serializer = self.get_serializer(data=request.data)
    #     if purchase_order_serializer.is_valid():
    #         user = self.request.user
    #         purchase_order_serializer.save(created_by=user)
    #         return DrfResponse( 
    #             data    = [purchase_order_serializer.data], 
    #             status  = status.HTTP_201_CREATED, 
    #             error   = {}, 
    #             response = {'response': 'purchase_order created successfully'},
    #             headers = {}
    #         ).to_json()
    #     # print(purchase_order_serializer.errors)
    #     return DrfResponse( 
    #         data    = [purchase_order_serializer.data], 
    #         status  = status.HTTP_400_BAD_REQUEST, 
    #         error   = [purchase_order_serializer.errors], 
    #         response = {'response': 'Something went wrong'},
    #         headers = {}
    #     ).to_json()
        

    def retrieve(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order_serializer = self.get_serializer(purchase_order)
        return DrfResponse(
            data    = [purchase_order_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order_serializer = self.get_serializer(purchase_order, data= request.data)
        user = self.request.user
        if purchase_order_serializer.is_valid():
            purchase_order_serializer.save(updated_by= user, updated_at=datetime.utcnow())

            return DrfResponse( 
                data    = [purchase_order_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'purchase_order updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [purchase_order_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [purchase_order_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def partial_update(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order_serializer = self.get_serializer(purchase_order, data= request.data, partial=True)
        if purchase_order_serializer.is_valid():
            purchase_order_serializer.save()

            return DrfResponse( 
                data    = [purchase_order_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'purchase_order updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [purchase_order_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [purchase_order_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        purchase_order = self.get_object()
        # purchase_order.delete()
        purchase_order_serializer = self.get_serializer(purchase_order, data= request.data)
        user = self.request.user
        if purchase_order_serializer.is_valid():
            purchase_order_serializer.save(updated_by= user, updated_at=datetime.utcnow(), is_active = 0)
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'purchase_order deleted successfully'},
            headers = {}
        ).to_json()
