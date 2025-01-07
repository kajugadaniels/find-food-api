from base.models import *
from account.models import *
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.
    """

    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('SEO'), {
            'fields': ('slug',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """
    Admin interface for the Place model.
    """
    list_display = (
        'user_name',
        'category',
        'main_phone_number',
        'email',
        'created_at',
        'updated_at',
        'profile_image_thumbnail',
    )
    search_fields = ('user__email', 'user__name', 'address', 'category__name')
    list_filter = ('category', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'profile_image_preview')

    fieldsets = (
        (_('User Information'), {
            'fields': ('user', 'profile_image_preview')
        }),
        (_('Place Details'), {
            'fields': ('category', 'description', 'address', 'latitude', 'longitude')
        }),
        (_('Contact Information'), {
            'fields': ('main_phone_number', 'second_phone_number', 'email')
        }),
        (_('Social Media'), {
            'fields': ('instagram', 'whatsapp', 'tiktok', 'facebook', 'twitter')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def user_name(self, obj):
        """
        Displays the associated user's name.
        """
        return obj.user.name if obj.user else '-'
    user_name.short_description = 'User Name'

    def profile_image_thumbnail(self, obj):
        """
        Displays a thumbnail of the profile image in the list view.
        """
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />',
                obj.profile_image.url
            )
        return '-'
    profile_image_thumbnail.short_description = 'Profile Image'

    def profile_image_preview(self, obj):
        """
        Displays a larger preview of the profile image in the detail view.
        """
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 50%;" />',
                obj.profile_image.url
            )
        return '-'
    profile_image_preview.short_description = 'Profile Image Preview'

    def get_queryset(self, request):
        """
        Optimizes the queryset by selecting related user and category.
        """
        return super().get_queryset(request).select_related('user', 'category')

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Mark selected places as active')
    def make_active(self, request, queryset):
        queryset.update(user__is_active=True)

    @admin.action(description='Mark selected places as inactive')
    def make_inactive(self, request, queryset):
        queryset.update(user__is_active=False)