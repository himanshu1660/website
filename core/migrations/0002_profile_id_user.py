# Generated by Django 5.0.2 on 2024-04-01 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='id_user',
            field=models.IntegerField(default=0),
        ),
    ]
