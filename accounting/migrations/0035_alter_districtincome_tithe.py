# Generated by Django 5.0.2 on 2024-02-26 20:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0034_districtincome_tithe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='districtincome',
            name='tithe',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tithe_from_church', to='accounting.combinedoffering'),
        ),
    ]
