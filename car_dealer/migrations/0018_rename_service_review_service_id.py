# Generated by Django 4.2.7 on 2023-11-19 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0017_remove_review_service_id_review_service_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='service',
            new_name='service_id',
        ),
    ]