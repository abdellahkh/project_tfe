# Generated by Django 5.1.1 on 2024-12-01 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0035_review_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='voiture',
            name='num_chassis',
            field=models.TextField(blank=True, help_text='Chassis de la voiture', null=True),
        ),
    ]
