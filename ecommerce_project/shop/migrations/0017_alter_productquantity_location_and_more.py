# Generated by Django 4.2.5 on 2024-03-14 15:46

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_productimages_main'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productquantity',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productquantity', to='shop.productlocation'),
        ),
        migrations.AlterField(
            model_name='productquantity',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_quantity', to='shop.product'),
        ),
        migrations.AddConstraint(
            model_name='productquantity',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('product'), django.db.models.functions.text.Lower('location'), name='unique_product_location'),
        ),
    ]
