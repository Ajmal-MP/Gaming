# Generated by Django 4.1 on 2022-10-03 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0018_remove_coupon_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='user',
        ),
    ]