from django.db.models import (
    Model,
    CASCADE,
    PROTECT,
    CharField,
    TextChoices,
    ForeignKey,
    PositiveSmallIntegerField, Sum, F,
)


class Shipment(Model):
    class Status(TextChoices):
        DRAFT = 'draft', 'План'
        SUCCEEDED = 'succeeded', 'Проведена'
        FAILED = 'failed', 'Отклонена'

    status = CharField(
        'статус',
        max_length=30,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    vendor = CharField(
        'поставщик',
        max_length=255,
    )

    @property
    def amount(self):
        return self.shipmentitem_set.all().aggregate(
            amount=Sum(F('price') * F('count'))
        )['amount'] or 0

    amount.fget.short_description = 'итоговая сумма'

    def __str__(self):
        return f'Заявка № {self.id}'

    class Meta:
        verbose_name = 'заявку'
        verbose_name_plural = 'закупка'
        ordering = ('status',)


class ShipmentItem(Model):
    shipment = ForeignKey(
        'Shipment',
        verbose_name='заявка',
        on_delete=CASCADE,
    )
    inventory = ForeignKey(
        'Inventory',
        verbose_name='инвентарь',
        on_delete=PROTECT,
    )
    price = PositiveSmallIntegerField(
        'цена',
        default=1000,
    )
    count = PositiveSmallIntegerField(
        'количество',
        default=1,
    )

    @property
    def amount(self):
        return self.count * self.price

    amount.fget.short_description = 'сумма'

    def __str__(self):
        return f'{self.inventory} — {self.count}'

    class Meta:
        verbose_name = 'инвентарь'
        verbose_name_plural = 'позиции'
        unique_together = (
            ('shipment', 'inventory'),
        )
