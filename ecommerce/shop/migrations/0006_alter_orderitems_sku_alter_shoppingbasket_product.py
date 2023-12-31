# Generated by Django 4.2.5 on 2023-10-12 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_shoppingbasket_quantity_alter_order_billing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='sku',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='shoppingbasket',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_basket', to='shop.product'),
        ),
    ]
