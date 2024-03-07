# Generated by Django 5.0.2 on 2024-02-23 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_member_member_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quarter',
            name='tag',
            field=models.CharField(choices=[('1st_Quarter', '1st_Quarter'), ('2nd_Quarter', '2nd_Quarter'), ('3rd_Quarter', '3rd_Quarter'), ('4th_Quarter', '4th_Quarter')], default='1st_Quarter', max_length=20, unique=True),
        ),
    ]
