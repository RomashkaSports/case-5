from django.contrib.admin import SimpleListFilter

from src.storage.models import Shipment, Order, Repair


class StatusBaseFilter(SimpleListFilter):
    title = 'Статус заявок'
    base_filter = 'all'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            (None, 'Все заявки'),
        )

    def get_facet_counts(self, pk_attname, filtered_qs):
        value = self.value
        count = {}
        for lookup, title in self.lookup_choices:
            self.value = lambda: lookup
            count[lookup] = self.queryset(None, filtered_qs).count()
        self.value = value
        return count

    def choices(self, cl):
        queryset = cl.get_queryset(self.request, exclude_parameters=self.expected_parameters())
        facets = self.get_facet_counts(None, queryset) if cl.add_facets else {}
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title + f' ({facets.get(lookup)})' if facets else title,
            }

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.filter(
                status=self.base_filter
            )
        if self.value() == 'all':
            return queryset
        return queryset.filter(status=self.value())


class StatusShipmentFilter(StatusBaseFilter):
    base_filter = Shipment.Status.DRAFT

    def lookups(self, request, model_admin):
        return (
            (None, 'Запланированные'),
            (Shipment.Status.SUCCEEDED, 'Успешные'),
            (Shipment.Status.FAILED, 'Отклонённые'),
            ('all', 'Все заявки'),
        )


class StatusOrderFilter(StatusBaseFilter):
    base_filter = Order.Status.CREATED

    def lookups(self, request, model_admin):
        return (
            (None, 'Новые'),
            (Order.Status.ACTIVE, 'Активные'),
            (Order.Status.RETURNED, 'Закрытые'),
            (Order.Status.CANCEL, 'Отменённые'),
            ('all', 'Все заявки'),
        )


class StatusRepairFilter(StatusBaseFilter):
    base_filter = Repair.Status.IN_PROGRESS

    def lookups(self, request, model_admin):
        return (
            (None, 'В ремонте'),
            (Repair.Status.DONE, 'Закрытые'),
            (Repair.Status.TRASH, 'Списанные'),
            ('all', 'Все заявки'),
        )
