# Generated by Django 4.1 on 2022-09-27 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0008_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_offer',
            field=models.CharField(max_length=255),
        ),
    ]
