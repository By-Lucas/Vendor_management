# Generated by Django 4.1.5 on 2023-01-07 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
