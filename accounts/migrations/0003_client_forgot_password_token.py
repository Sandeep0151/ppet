# Generated by Django 4.2.6 on 2023-10-30 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='forgot_password_token',
            field=models.CharField(default='', max_length=100),
        ),
    ]