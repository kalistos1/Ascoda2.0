# Generated by Django 5.0.2 on 2024-02-21 05:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0023_alter_totaltoconference_church'),
        ('accounts', '0016_alter_member_member_email_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AmountDueDistrict',
        ),
        migrations.AddField(
            model_name='trustfund',
            name='church',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='accounts.church'),
        ),
        migrations.AlterField(
            model_name='totaltoconference',
            name='church',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.church'),
        ),
    ]
