# Generated by Django 4.2.6 on 2023-11-08 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_appointment_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='signature_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]