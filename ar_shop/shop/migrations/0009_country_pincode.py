# Generated by Django 3.1 on 2021-01-30 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_customeraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pincode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pincode', models.CharField(max_length=100)),
            ],
        ),
    ]
