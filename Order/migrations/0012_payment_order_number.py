# Generated by Django 4.1 on 2022-09-30 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0011_coupon_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order_number',
            field=models.IntegerField(default=12345678),
            preserve_default=False,
        ),
    ]
