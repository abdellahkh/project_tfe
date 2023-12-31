# Generated by Django 4.2.7 on 2023-11-22 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0002_alter_member_postal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='address',
            field=models.CharField(blank=True, help_text='adresse', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(blank=True, help_text='Phone', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='ville',
            field=models.CharField(blank=True, help_text='Ville', max_length=100, null=True),
        ),
    ]
