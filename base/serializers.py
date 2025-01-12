from base.models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Place model.
    """

    user_slug = serializers.ReadOnlyField(source='user.slug', read_only=True)
    user_name = serializers.ReadOnlyField(source='user.name', read_only=True)

    class Meta:
        model = Place
        fields = '__all__'