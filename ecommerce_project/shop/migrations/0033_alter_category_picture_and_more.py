# Generated by Django 4.2.5 on 2024-04-02 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0032_alter_productimages_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='picture',
            field=models.ImageField(default='img/categories/default.png', upload_to='C:\\pythonProjects\\finalproject\\ecommerce_project\\shop/static/img/categories/'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='image_name',
            field=models.ImageField(max_length=1000, upload_to='C:\\pythonProjects\\finalproject\\ecommerce_project\\shop/static/img/products/'),
        ),
    ]
