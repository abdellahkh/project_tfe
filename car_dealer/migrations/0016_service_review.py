# Generated by Django 4.2.7 on 2023-11-19 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car_dealer', '0015_voiture_reserve'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(help_text='Nom du modèle', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Commentaire', null=True)),
                ('prix', models.DecimalField(decimal_places=0, help_text='Prix de la voiture', max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, help_text='Commentaire', null=True)),
                ('service_id', models.ForeignKey(help_text='Identifiant du User qui a commenté', on_delete=django.db.models.deletion.CASCADE, to='car_dealer.service')),
                ('user_id', models.ForeignKey(help_text='Identifiant du User qui a commenté', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
