# Generated by Django 2.0.3 on 2018-05-01 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_remove_user_projects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='subject',
            field=models.CharField(max_length=200),
        ),
    ]