# Generated by Django 3.1 on 2021-01-30 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20210130_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraddress',
            name='phone',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='phone',
            field=models.CharField(max_length=13),
        ),
    ]
