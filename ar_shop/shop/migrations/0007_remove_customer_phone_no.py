# Generated by Django 3.1.3 on 2020-12-04 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_customer_phone_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phone_no',
        ),
    ]