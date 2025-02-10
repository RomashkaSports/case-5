from django.contrib.admin import (
    ModelAdmin,
    TabularInline,
    register,
)

from src.storage.filters import StatusOrderFilter
from src.storage.models import (
    Order,
    OrderItem,
)


class OrderItemInline(TabularInline):
    model = OrderItem
    min_num = 1
    extra = 0
    autocomplete_fields = (
        'inventory',
    )

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        if obj.status == obj.Status.CREATED:
            return True
        return False

    def has_add_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


@register(Order)
class OrderAdmin(ModelAdmin):
    inlines = (
        OrderItemInline,
    )
    list_display = (
        '__str__',
        'user',
        'status',
    )
    list_filter = (
        StatusOrderFilter,
    )
    readonly_fields = (
        'created_at',
        'start_date',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields
        if obj.status != obj.Status.CREATED:
            return (
                'user',
                'created_at',
                'start_date',
                'end_date',
            )
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        if obj.status in {obj.Status.CREATED, obj.Status.ACTIVE}:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return True
