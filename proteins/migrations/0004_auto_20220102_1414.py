# Generated by Django 3.0.3 on 2022-01-02 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proteins', '0003_auto_20220102_1412'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='domains',
            unique_together={('description', 'start', 'stop')},
        ),
    ]
