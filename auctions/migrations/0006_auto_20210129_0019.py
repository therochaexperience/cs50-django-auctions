# Generated by Django 3.1.5 on 2021-01-29 05:19

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210128_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='currentBid',
            field=models.DecimalField(decimal_places=2, default=0.01, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='listing',
            name='startingBid',
            field=models.DecimalField(decimal_places=2, default=0.01, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
