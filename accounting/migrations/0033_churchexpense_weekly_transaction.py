# Generated by Django 5.0.2 on 2024-02-26 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0032_remove_churchincome_offering_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='churchexpense',
            name='Weekly_transaction',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weeks_expense_sum', to='accounting.weeklytransaction'),
        ),
    ]
