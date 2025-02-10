from config import settings
from django.db.models import (
    Sum,
    Model,
    CASCADE,
    CharField,
    TextField,
    SlugField,
    ForeignKey,
)

from filebrowser.fields import FileBrowseField

from src.storage.models.orders import Order
from src.storage.models.repair import Repair
from src.storage.models.shipment import Shipment


class Category(Model):
    title = CharField(
        'категория',
        max_length=255,
        unique=True,
    )
    slug = SlugField(
        'URL',
        unique=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'


class Inventory(Model):
    category = ForeignKey(
        'Category',
        verbose_name='категория',
        on_delete=CASCADE,
    )
    title = CharField(
        'название',
        max_length=255,
    )
    description = TextField(
        'описание',
    )
    image = FileBrowseField(
        'изображение',
        extensions=settings.FILEBROWSER_EXTENSIONS['Image'],
        max_length=255,
        blank=True,
    )

    @property
    def count_in_active(self):
        return self.orderitem_set.filter(
            order__status__in=(
                Order.Status.CREATED,
                Order.Status.ACTIVE,
            )
        ).aggregate(count=Sum('count'))['count'] or 0

    @property
    def count_in_trash(self):
        return self.repairitem_set.filter(
            repair__status=Repair.Status.TRASH,
        ).aggregate(count=Sum('count'))['count'] or 0

    @property
    def count_in_repair(self):
        return self.repairitem_set.filter(
            repair__status=Repair.Status.IN_PROGRESS,
        ).aggregate(count=Sum('count'))['count'] or 0

    @property
    def count(self):
        full_items = self.shipmentitem_set.filter(
            shipment__status=Shipment.Status.SUCCEEDED,
        ).aggregate(count=Sum('count'))['count']
        return (full_items or 0) - self.count_in_trash

    @property
    def available(self):
        return self.count - self.count_in_active - self.count_in_repair

    count.fget.short_description = 'всего'
    available.fget.short_description = 'доступно'
    count_in_active.fget.short_description = 'забронировано'
    count_in_repair.fget.short_description = 'в ремонте'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'инвентарь'
        verbose_name_plural = 'инвентарь'
