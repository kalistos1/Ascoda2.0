# Generated by Django 5.0.3 on 2024-04-06 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0052_alter_churchincome_income_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='churchexpense',
            name='title',
            field=models.CharField(choices=[('10_PERCENT_DUE_DISTRICT', '10_PERCENT_DUE_DISTRICT'), ('40_PERCENT_DUE_CONFERENCE', '40_PERCENT_DUE_CONFERENCE'), ('OTHER_EXPENSE', 'OTHER_EXPENSE')], max_length=255),
        ),
    ]
