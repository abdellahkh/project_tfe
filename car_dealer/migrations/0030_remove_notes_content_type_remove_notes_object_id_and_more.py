# Generated by Django 5.1.1 on 2024-09-28 07:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0029_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='notes',
            name='object_id',
        ),
        migrations.AddField(
            model_name='notes',
            name='demande_id',
            field=models.ForeignKey(help_text='Demande lié à la note', null=True, on_delete=django.db.models.deletion.CASCADE, to='car_dealer.demande'),
        ),
        migrations.AddField(
            model_name='notes',
            name='vente_id',
            field=models.ForeignKey(help_text='Vente lié à la note', null=True, on_delete=django.db.models.deletion.CASCADE, to='car_dealer.vente'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='date',
            field=models.DateTimeField(auto_now_add=True, help_text='Date de la note', null=True),
        ),
    ]
