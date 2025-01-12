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

class PlaceSerializer(serializers.ModelSerializer):
    """
    Serializer for Place model.
    The 'user_slug' field is a read-only field representing the associated user's slug.
    """
    user_slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at', 'user_slug']

    def get_user_slug(self, obj):
        """
        Returns the slug of the associated user.
        """
        return obj.user.slug if obj.user else None

    def create(self, validated_data):
        """
        Create a new Place instance.
        Note: The Place model's save() method handles auto-creation of a User (with role 'Client') if not provided.
        """
        place = Place.objects.create(**validated_data)
        return place

    def update(self, instance, validated_data):
        """
        Update an existing Place instance with validated data.
        If the profile_image is updated, the method also updates the associated user's image.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Ensure that if profile_image is updated, the associated user's image reflects this change.
        if 'profile_image' in validated_data and instance.user:
            instance.user.image = validated_data.get('profile_image')
            instance.user.save()
        return instance