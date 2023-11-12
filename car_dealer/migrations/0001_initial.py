# Generated by Django 4.2.7 on 2023-11-12 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Marque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(help_text='Nom de la marque', max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Modele',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(help_text='Nom du modèle', max_length=100)),
                ('marque', models.ForeignKey(help_text='Marque à laquelle le modèle appartient', on_delete=django.db.models.deletion.CASCADE, to='car_dealer.marque')),
            ],
        ),
        migrations.CreateModel(
            name='Voiture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee_fabrication', models.PositiveIntegerField(help_text='Année de fabrication')),
                ('kilometrage', models.PositiveIntegerField(help_text='Kilométrage actuel')),
                ('prix', models.DecimalField(decimal_places=2, help_text='Prix de la voiture', max_digits=10)),
                ('description', models.TextField(blank=True, help_text='Description de la voiture', null=True)),
                ('date_poste', models.DateTimeField(auto_now_add=True, help_text="Date de publication de l'annonce")),
                ('proprietaire', models.CharField(help_text='Nom du propriétaire actuel', max_length=100)),
                ('image', models.ImageField(blank=True, help_text='Image de la voiture', null=True, upload_to='images/voitures/')),
                ('marque', models.ForeignKey(help_text='Marque de la voiture', on_delete=django.db.models.deletion.CASCADE, related_name='voitures', to='car_dealer.marque')),
                ('modele', models.OneToOneField(help_text='Modèle de la voiture', on_delete=django.db.models.deletion.CASCADE, to='car_dealer.modele')),
            ],
            options={
                'ordering': ['-date_poste'],
            },
        ),
    ]
