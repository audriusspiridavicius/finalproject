# Generated by Django 4.2.5 on 2024-02-10 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_remove_productquantity_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productprices',
            name='date_created',
        ),
    ]
