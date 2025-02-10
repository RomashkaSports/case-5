from django.db.models import (
    Model,
    CASCADE,
    PROTECT,
    CharField,
    TextField,
    TextChoices,
    ForeignKey,
    PositiveSmallIntegerField,
)


class Repair(Model):
    class Status(TextChoices):
        IN_PROGRESS = 'in_progress', 'В ремонте'
        DONE = 'done', 'Отремонтировано'
        TRASH = 'trash', 'Списано'

    status = CharField(
        'статус',
        max_length=30,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
    )
    description = TextField(
        'комментарий',
        blank=True,
    )

    def __str__(self):
        return f'Заявка на ремонт № {self.id}'

    class Meta:
        verbose_name = 'заявку'
        verbose_name_plural = 'ремонт'
        ordering = ('status',)


class RepairItem(Model):
    repair = ForeignKey(
        'Repair',
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

    def __str__(self):
        return f'{self.inventory} — {self.count}'

    class Meta:
        verbose_name = 'инвентарь'
        verbose_name_plural = 'позиции'
        unique_together = (
            ('repair', 'inventory'),
        )
