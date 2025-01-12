from base.models import *
from account.models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Create a new Category instance. The model's save method auto-generates a unique slug if not provided.
        """
        category = Category.objects.create(**validated_data)
        return category