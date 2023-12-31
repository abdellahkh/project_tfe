# Generated by Django 4.2.7 on 2023-11-28 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0008_demande_car_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='date_desiree',
            field=models.DateField(blank=True, help_text="  (Date d'intervention souhaitée)", null=True),
        ),
        migrations.AlterField(
            model_name='voituresoumisse',
            name='date_poste',
            field=models.DateField(auto_now_add=True, help_text="Date de publication de l'annonce"),
        ),
    ]
