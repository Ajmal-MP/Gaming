# Generated by Django 4.1 on 2022-10-04 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Category', '0003_categories_category_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='categories',
            name='slug',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
