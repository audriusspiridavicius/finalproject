# Generated by Django 5.0.2 on 2024-03-03 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_productquantity_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productquantity',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_quantity', to='shop.productlocation'),
        ),
    ]
