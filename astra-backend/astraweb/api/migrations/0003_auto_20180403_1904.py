# Generated by Django 2.0.3 on 2018-04-04 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180401_2339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='area1',
            new_name='area',
        ),
        migrations.RemoveField(
            model_name='project',
            name='area2',
        ),
    ]