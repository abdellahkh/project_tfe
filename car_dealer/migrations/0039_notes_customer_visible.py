# Generated by Django 5.1.1 on 2024-12-04 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0038_alter_vente_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='customer_visible',
            field=models.BooleanField(default=False, help_text='Visible par le membre'),
        ),
    ]