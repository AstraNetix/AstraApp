# Generated by Django 2.0.3 on 2018-04-12 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20180411_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id_file',
        ),
        migrations.RemoveField(
            model_name='user',
            name='selfie',
        ),
    ]