# Generated by Django 2.0.3 on 2018-03-29 23:47

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180327_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bitcoin_balance',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=11, validators=[django.core.validators.MinValueValidator(Decimal('0.0000'))]),
        ),
        migrations.AlterField(
            model_name='user',
            name='ether_balance',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=11, validators=[django.core.validators.MinValueValidator(Decimal('0.0000'))]),
        ),
        migrations.AlterField(
            model_name='user',
            name='star_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='user',
            name='usd_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
