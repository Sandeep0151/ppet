# Generated by Django 4.2.6 on 2023-10-31 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_appointment_drop_location_appointment_instructions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='drop_location',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='instructions',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='pet_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='pickup_location',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
