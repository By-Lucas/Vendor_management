# Generated by Django 4.1.5 on 2023-01-07 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_category_category_name_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='vendor',
        ),
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
    ]
