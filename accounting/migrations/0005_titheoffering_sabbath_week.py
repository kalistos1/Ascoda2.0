# Generated by Django 5.0.1 on 2024-02-15 21:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_remove_titheoffering_card_number'),
        ('accounts', '0012_member_tithe_card_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='titheoffering',
            name='sabbath_week',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.sabbath'),
        ),
    ]
