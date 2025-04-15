from rest_framework import serializers
from category.models import Category

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id', 'title', 'description', 'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at', 'created_by']
