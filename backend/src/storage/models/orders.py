from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import (
    Model,
    CASCADE,
    PROTECT,
    CharField,
    TextChoices,
    ForeignKey,
    DateField,
    DateTimeField,
    PositiveSmallIntegerField,
)
from django.urls import reverse


class Order(Model):
    class Status(TextChoices):
        CREATED = 'created', 'Создано'
        ACTIVE = 'active', 'Выдано'
        RETURNED = 'returned', 'Возвращено'
        CANCEL = 'cancel', 'Отклонено'

    user = ForeignKey(
        'accounts.User',
        verbose_name='пользователь',
        on_delete=PROTECT,
    )
    status = CharField(
        'статус',
        max_length=30,
        choices=Status.choices,
        default=Status.CREATED,
    )
    created_at = DateTimeField(
        'создана',
        auto_now_add=True,
    )
    start_date = DateTimeField(
        'дата выдачи',
        null=True,
        editable=False,
    )
    end_date = DateField(
        'дата возврата',
    )

    def clean(self):
        if self.status == self.Status.ACTIVE and not self.start_date:
            self.start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.status == self.Status.RETURNED:
            self.end_date = datetime.now().strftime('%Y-%m-%d')

    def css(self):
        CSS = {
            self.Status.CREATED.value: 'primary',
            self.Status.ACTIVE.value: 'info',
            self.Status.RETURNED.value: 'success',
            self.Status.CANCEL.value: 'secondary',
        }
        return CSS.get(self.status, 'primary')

    def __str__(self):
        return f'Заявка № {self.id}'

    def items(self):
        return self.orderitem_set.all()

    def get_absolute_url(self):
        return reverse('storage:order_detail', kwargs={
            'pk': self.id,
        })

    class Meta:
        verbose_name = 'заявку'
        verbose_name_plural = 'выдача инвентаря'
        ordering = ('status', '-created_at')


class OrderItem(Model):
    order = ForeignKey(
        'Order',
        verbose_name='заявка',
        on_delete=CASCADE,
    )
    inventory = ForeignKey(
        'Inventory',
        verbose_name='инвентарь',
        on_delete=PROTECT,
    )
    count = PositiveSmallIntegerField(
        'количество',
        default=1,
    )

    def clean(self):
        try:
            available = self.inventory.available
            if self.pk:
                available += self.count
            if self.count > available:
                raise ValidationError(f'Доступно инвентаря {available} шт.')
        except AttributeError:
            available = 0

    def __str__(self):
        return f'{self.inventory} — {self.count}'

    class Meta:
        verbose_name = 'инвентарь'
        verbose_name_plural = 'позиции'
        unique_together = (
            ('order', 'inventory'),
        )
