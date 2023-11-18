# Generated by Django 4.2.7 on 2023-11-12 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0011_alter_voiture_parkassist'),
    ]

    operations = [
        migrations.AddField(
            model_name='voiture',
            name='sold',
            field=models.BooleanField(default=False, verbose_name='Vendu'),
        ),
        migrations.AlterField(
            model_name='voiture',
            name='carburant',
            field=models.CharField(blank=True, choices=[('Diesel', 'Diesel'), ('Essence', 'Essence'), ('Ethanol', 'Ethanol'), ('Electrique', 'Electrique'), ('Hydrogene', 'Hydrogene'), ('LPG', 'LPG'), ('CNG', 'CNG'), ('Hybride (Elec - Ess)', 'Hybride (Elec - Ess)'), ('Hybride (Elec - Diesel)', 'Hybride (Elec - Diesel)'), ('Autres', 'Autres')], help_text='Type de carburant de la voiture', max_length=90, null=True),
        ),
    ]