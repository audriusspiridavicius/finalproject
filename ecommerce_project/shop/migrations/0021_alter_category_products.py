# Generated by Django 4.2.5 on 2024-03-25 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_alter_category_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(to='shop.product'),
        ),
    ]