# Generated by Django 4.2.5 on 2024-02-24 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_remove_productimages_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimages',
            name='main',
            field=models.BooleanField(default=False),
        ),
    ]