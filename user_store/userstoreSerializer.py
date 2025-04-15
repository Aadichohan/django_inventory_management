from rest_framework import serializers
from user_store.models import UserStore

from user.userSerializer import UserSerializer
from store.storeSerializer import StoreSerializer

class UserStoreSerializer(serializers.ModelSerializer):

    user_id = serializers.CharField()
    store_id = serializers.CharField()

    user_data = UserSerializer(source='user', read_only=True)
    store_data = StoreSerializer(source='store', read_only=True)

    class Meta:
        model = UserStore
        fields = [
            'id', 'user_id','user_data', 'store_id', 'store_data',
            'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at']