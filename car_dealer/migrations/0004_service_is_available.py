# Generated by Django 4.2.7 on 2023-11-23 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0003_alter_member_address_alter_member_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='is_available',
            field=models.BooleanField(default=False, verbose_name='Disponible'),
        ),
    ]
