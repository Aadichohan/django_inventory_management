
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, response
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.utils import timezone

from decimal import Decimal

from sales_order.models import SalesOrder
from store_product.models import StoreProduct
from sales_order.salesOrderSerializer import SalesOrderSerializer
from django_inventory_management.response import DrfResponse
from role_permission.role_based_permission import RoleBasedPermission

class SalesOrderViewSet(ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        sales_order = SalesOrder.objects.all()
        sales_order_serializer = SalesOrderSerializer(sales_order, many=True)
        # print(sales_order_serializer)
        return DrfResponse(
            data    = sales_order_serializer.data, 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    # def create(self, request):
    #     sales_order_serializer = self.get_serializer(data=request.data)
    #     if sales_order_serializer.is_valid():
    #         user = self.request.user
    #         sales_order_serializer.save(created_by=user)
    #         return DrfResponse( 
    #             data    = [sales_order_serializer.data], 
    #             status  = status.HTTP_201_CREATED, 
    #             error   = {}, 
    #             response = {'response': 'sales_order created successfully'},
    #             headers = {}
    #         ).to_json()
    #     # print(sales_order_serializer.errors)
    #     return DrfResponse( 
    #         data    = [sales_order_serializer.data], 
    #         status  = status.HTTP_400_BAD_REQUEST, 
    #         error   = [sales_order_serializer.errors], 
    #         response = {'response': 'Something went wrong'},
    #         headers = {}
    #     ).to_json()
    def create(self, request):
        try:
            user = request.user
            store_id = request.data.get('store_id')
            product_id = request.data.get('product_id')

            store_product = StoreProduct.objects.get(store_id=store_id, product_id=product_id)

            quantity = Decimal(str(request.data.get('quantity', 0)))
            sell_price = store_product.sell_price
            total_price = quantity * sell_price if quantity and sell_price else 0.00

            data = request.data.copy()
            data['total_price'] = total_price
            data['sell_price'] = sell_price

            sales_order_serializer = self.get_serializer(data=data, context={'request': request})

            if sales_order_serializer.is_valid():
                sales_order = sales_order_serializer.save(created_by=user)
                store_product.quantity -= quantity
                store_product.updated_by = user
                store_product.updated_at = datetime.utcnow()
                store_product.save()

                return DrfResponse(
                    data=[sales_order_serializer.data],
                    status=status.HTTP_201_CREATED,
                    response={"response": "Sales order created successfully"},
                    error={}, headers={}
                ).to_json()
            else:
                # print("Serializer Errors: ", sales_order_serializer.errors)
                return DrfResponse(
                    data=[],
                    status=status.HTTP_400_BAD_REQUEST,
                    error=[sales_order_serializer.errors],
                    response={"response": "Validation failed"},
                    headers={}
                ).to_json()

        except (Exception, StoreProduct.DoesNotExist) as e:
            print("Error:", str(e))
            return DrfResponse(
                data=[],
                status=status.HTTP_400_BAD_REQUEST,
                error=[str(e)],  # ✅ Converted to string
                response={"response": "Something went wrong"},
                headers={}
            ).to_json()


    def retrieve(self, request, pk=None):
        sales_order = self.get_object()
        sales_order_serializer = self.get_serializer(sales_order)
        return DrfResponse(
            data    = [sales_order_serializer.data], 
            status  = status.HTTP_200_OK, 
            error   = {}, 
            headers = {}
        ).to_json()

    def update(self, request, pk=None):
        try:
            sales_order = self.get_object()
            # print('sales_order ', sales_order.quantity)
            user = request.user
            store_id = request.data.get('store_id')
            product_id = request.data.get('product_id')

            store_product = StoreProduct.objects.get(store_id=store_id, product_id=product_id)

            quantity = Decimal(str(request.data.get('quantity', 0)))
            sell_price = store_product.sell_price
            total_price = quantity * sell_price if quantity and sell_price else 0.00
            data = request.data.copy()
            data['total_price'] = total_price
            data['sell_price'] = sell_price
            data['quantity'] = quantity
            sales_order_serializer = self.get_serializer(sales_order, data= data)
            # user = self.request.user
            if sales_order_serializer.is_valid():
                sales_order_quantity = sales_order.quantity
                sales_order = sales_order_serializer.save(updated_by= user, updated_at=timezone.now())
                # final_quantity = 0
                # print('sales_order.quantity > quantity',sales_order_quantity > quantity)
                # print('sales_order.quantity < quantity',sales_order_quantity < quantity)
                # print('sales_order.quantity',sales_order_quantity )
                # print('quantity', quantity )
                if sales_order_quantity > quantity:
                    remaining_quantity =sales_order_quantity - quantity
                    final_quantity = store_product.quantity + remaining_quantity
                    print('sales_order.quantity > quantity: ',final_quantity)

                    store_product.quantity = final_quantity
                    store_product.updated_by = user
                    store_product.updated_at = timezone.now()
                    store_product.save()
                elif sales_order_quantity < quantity:
                    remaining_quantity = quantity - sales_order_quantity
                    final_quantity = store_product.quantity - remaining_quantity
                    print('sales_order.quantity < quantity: ',final_quantity)

                    store_product.quantity = final_quantity
                    store_product.updated_by = user
                    store_product.updated_at = timezone.now()
                    store_product.save()

                return DrfResponse( 
                    data    = [sales_order_serializer.data], 
                    status  = status.HTTP_200_OK, 
                    error   = {}, 
                    response = {'response': 'sales_order updated successfully'},
                    headers = {}
                ).to_json()
        
        except (Exception, StoreProduct.DoesNotExist) as e:
            print("Error:", str(e))
            return DrfResponse(
                data=[],
                status=status.HTTP_400_BAD_REQUEST,
                error=[str(e)],  # ✅ Converted to string
                response={"response": "Something went wrong"},
                headers={}
            ).to_json()
    
    def partial_update(self, request, pk=None):
        sales_order = self.get_object()
        sales_order_serializer = self.get_serializer(sales_order, data= request.data, partial=True)
        if sales_order_serializer.is_valid():
            sales_order_serializer.save()

            return DrfResponse( 
                data    = [sales_order_serializer.data], 
                status  = status.HTTP_200_OK, 
                error   = {}, 
                response = {'response': 'sales_order updated successfully'},
                headers = {}
            ).to_json()
        
        return DrfResponse( 
            data    = [sales_order_serializer.data], 
            status  = status.HTTP_400_BAD_REQUEST, 
            error   = [sales_order_serializer.errors], 
            response = {'response': 'Something went wrong'},
            headers = {}
        ).to_json()

    def destroy(self, request, pk=None):
        sales_order = self.get_object()
        user = self.request.user
        # sales_order.delete()
        data = {
            "is_active": 0,
            "updated_by": user.pk,
            "updated_at": datetime.utcnow()
        }
        sales_order_serializer = self.get_serializer(sales_order, data= data, partial=True)
        if sales_order_serializer.is_valid():
            sales_order_serializer.save()
        return DrfResponse( 
         
            status  = status.HTTP_204_NO_CONTENT, 
            error   = {}, 
            response = {'response': 'sales_order deleted successfully'},
            headers = {}
        ).to_json()
