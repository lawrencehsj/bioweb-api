# Generated by Django 3.0.3 on 2022-01-02 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proteins', '0006_auto_20220102_1459'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taxonomy',
            old_name='taxo_id',
            new_name='taxa_id',
        ),
    ]
