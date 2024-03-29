# Generated by Django 5.0.2 on 2024-02-20 23:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0021_rename_others_churchexpense_amount_and_more'),
        ('accounts', '0016_alter_member_member_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='churchcashaccount',
            name='church',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='accounts.church'),
        ),
        migrations.AddField(
            model_name='churchexpense',
            name='church',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='accounts.church'),
        ),
        migrations.AddField(
            model_name='churchincome',
            name='church',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='accounts.church'),
        ),
    ]
