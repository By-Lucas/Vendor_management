# Generated by Django 4.1.5 on 2023-01-15 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_image_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_product',
            field=models.ImageField(blank=True, null=True, upload_to='product'),
        ),
    ]
