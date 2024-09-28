# Generated by Django 5.1.1 on 2024-09-27 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0027_voiture_favoris'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voiture',
            name='status',
            field=models.CharField(choices=[('standby', 'Standby'), ('avendre', 'A vendre'), ('ready', 'Ready'), ('reservé', 'Reservé'), ('transit', 'transit'), ('vendu', 'Vendu')], default='standby', help_text='Statut de la voiture', max_length=10),
        ),
    ]
