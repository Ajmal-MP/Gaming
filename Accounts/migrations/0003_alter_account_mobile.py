# Generated by Django 4.1 on 2022-09-23 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_remove_account_otp_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='mobile',
            field=models.CharField(max_length=14, unique=True),
        ),
    ]
