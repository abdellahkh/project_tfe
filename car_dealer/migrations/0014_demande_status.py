# Generated by Django 4.2.7 on 2023-12-03 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0013_alter_demande_car_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='status',
            field=models.CharField(blank=True, choices=[('Actif', 'Actif'), ('Information', 'Information'), ('Close', 'Close')], default='Actif', help_text='Type de service', max_length=90, null=True),
        ),
    ]
