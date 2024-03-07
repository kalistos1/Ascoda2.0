# Generated by Django 5.0.1 on 2024-02-16 05:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0006_churchincome_date_added'),
        ('accounts', '0012_member_tithe_card_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='churchexpense',
            name='sabbath',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='accounts.sabbath'),
        ),
    ]
