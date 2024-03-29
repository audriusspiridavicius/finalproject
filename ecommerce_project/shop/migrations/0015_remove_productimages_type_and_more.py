# Generated by Django 4.2.5 on 2024-02-18 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_productimages_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimages',
            name='type',
        ),
        migrations.RemoveField(
            model_name='productquantity',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='productquantity',
            name='date_last_modified',
        ),
        migrations.AddField(
            model_name='orderitems',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productlocation',
            name='address',
            field=models.CharField(max_length=500),
        ),
    ]
