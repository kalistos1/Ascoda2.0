# Generated by Django 5.0.2 on 2024-02-19 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_rename_sabbath_date_sabbath_sabbath_week_ends'),
    ]

    operations = [
        migrations.AddField(
            model_name='sabbath',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
