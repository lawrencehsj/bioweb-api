# Generated by Django 3.0.3 on 2022-01-02 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proteins', '0004_auto_20220102_1414'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='domains',
            unique_together=set(),
        ),
    ]