# Generated by Django 5.1.1 on 2024-09-28 07:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0030_remove_notes_content_type_remove_notes_object_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='demande_id',
            field=models.ForeignKey(blank=True, help_text='Demande lié à la note', null=True, on_delete=django.db.models.deletion.CASCADE, to='car_dealer.demande'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='vente_id',
            field=models.ForeignKey(blank=True, help_text='Vente lié à la note', null=True, on_delete=django.db.models.deletion.CASCADE, to='car_dealer.vente'),
        ),
    ]
