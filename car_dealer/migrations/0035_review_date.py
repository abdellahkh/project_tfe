# Generated by Django 5.1.1 on 2024-12-01 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0034_rename_products_userwishlist_voiture'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateTimeField(auto_now_add=True, help_text='Date de création du commentaire', null=True),
        ),
    ]
