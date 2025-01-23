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
    Enhanced serializer for the Place model with expanded fields
    to directly return user and category information.
    """

    # User-related fields
    user_name = serializers.SerializerMethodField(read_only=True)
    user_email = serializers.SerializerMethodField(read_only=True)
    user_phone = serializers.SerializerMethodField(read_only=True)
    user_slug = serializers.SerializerMethodField(read_only=True)
    user_image = serializers.SerializerMethodField(read_only=True)

    # Category-related fields
    category_name = serializers.SerializerMethodField(read_only=True)
    category_slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Place
        fields = [

            'user_name',
            'user_email',
            'user_phone',
            'user_slug',
            'user_image',

            'category_name',
            'category_slug',

            'id',
            'description',
            'province',
            'district',
            'sector',
            'cell',
            'village',
            'address',
            'latitude',
            'longitude',
            'main_phone_number',
            'second_phone_number',
            'email',
            'instagram',
            'whatsapp',
            'tiktok',
            'facebook',
            'twitter',
            'profile_image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'user_name',
            'user_email',
            'user_phone',
            'user_slug',
            'user_image',
            'category_name',
            'category_slug',
        ]

    def get_user_name(self, obj):
        return obj.user.name if obj.user else None

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None

    def get_user_phone(self, obj):
        return obj.user.phone_number if obj.user else None

    def get_user_slug(self, obj):
        return obj.user.slug if obj.user else None

    def get_user_image(self, obj):
        """
        Return the full URL for the user's image if available,
        or None if the user/image is absent.
        """
        if obj.user and obj.user.image:
            return obj.user.image.url
        return None

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_category_slug(self, obj):
        return obj.category.slug if obj.category else None