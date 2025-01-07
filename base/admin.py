from base.models import *
from django.contrib import admin
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
