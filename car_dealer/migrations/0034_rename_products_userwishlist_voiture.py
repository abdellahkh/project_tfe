# Generated by Django 5.1.1 on 2024-09-29 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0033_remove_voiture_favoris_userwishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userwishlist',
            old_name='products',
            new_name='voiture',
        ),
    ]