from django.contrib.admin import (
    ModelAdmin,
    register,
)

from src.storage.models import (
    Category,
    Inventory,
)


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        'title',
        'slug',
    )
    prepopulated_fields = {
        'slug': ('title',)
    }
    search_fields = (
        'title',
        'slug',
    )


@register(Inventory)
class InventoryAdmin(ModelAdmin):
    save_as = True
    list_display = (
        'title',
        'count',
        'available',
        'count_in_active',
        'count_in_repair',
    )
    list_filter = (
        'category',
    )
    autocomplete_fields = (
        'category',
    )
    search_fields = (
        'title',
    )
