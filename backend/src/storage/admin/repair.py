from django.contrib.admin import (
    ModelAdmin,
    TabularInline,
    register,
)

from src.storage.filters.status import StatusRepairFilter
from src.storage.models import (
    Repair,
    RepairItem,
)


class RepairItemInline(TabularInline):
    model = RepairItem
    min_num = 1
    extra = 0
    autocomplete_fields = (
        'inventory',
    )

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        return self.has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


@register(Repair)
class RepairAdmin(ModelAdmin):
    inlines = (
        RepairItemInline,
    )
    list_display = (
        '__str__',
        'status',
    )
    list_filter = (
        StatusRepairFilter,
    )

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        if obj.status != Repair.Status.IN_PROGRESS:
            return False
        return True
