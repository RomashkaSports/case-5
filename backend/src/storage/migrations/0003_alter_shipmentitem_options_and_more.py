# Generated by Django 5.0.6 on 2025-02-05 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_shipment_alter_inventory_category_shipmentitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shipmentitem',
            options={'verbose_name': 'инвентарь', 'verbose_name_plural': 'позиции'},
        ),
        migrations.AlterUniqueTogether(
            name='shipmentitem',
            unique_together={('shipment', 'inventory')},
        ),
    ]
