from django.contrib.admin import (
    ModelAdmin,
    TabularInline,
    register,
    action,
)

from src.storage.filters import StatusShipmentFilter
from src.storage.models import (
    Shipment,
    ShipmentItem,
)


@action(description="Провести выбранные заявки")
def make_succeeded(modeladmin, request, queryset):
    queryset.filter(
        status=Shipment.Status.DRAFT
    ).update(
        status=Shipment.Status.SUCCEEDED,
    )


@action(description="Отклонить заявки")
def make_failed(modeladmin, request, queryset):
    queryset.filter(
        status=Shipment.Status.DRAFT
    ).update(
        status=Shipment.Status.FAILED,
    )


class ShipmentItemInline(TabularInline):
    model = ShipmentItem
    min_num = 1
    extra = 0
    autocomplete_fields = (
        'inventory',
    )
    fields = (
        'inventory',
        'price',
        'count',
        'amount',
    )
    readonly_fields = (
        'amount',
    )


@register(Shipment)
class ShipmentAdmin(ModelAdmin):
    inlines = (
        ShipmentItemInline,
    )
    actions = (
        make_succeeded,
        make_failed,
    )
    list_display = (
        '__str__',
        'status',
        'vendor',
        'amount',
    )
    readonly_fields = (
        'amount',
    )
    list_filter = (
        StatusShipmentFilter,
    )

    def has_change_permission(self, request, obj=None):
        if obj and obj.status != Shipment.Status.DRAFT:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return True
