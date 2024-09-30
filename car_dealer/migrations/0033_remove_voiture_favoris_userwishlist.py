# Generated by Django 5.1.1 on 2024-09-29 17:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0032_alter_demande_date_alter_voiture_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voiture',
            name='favoris',
        ),
        migrations.CreateModel(
            name='UserWishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(blank=True, related_name='product_favourite', to='car_dealer.voiture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favourite', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
