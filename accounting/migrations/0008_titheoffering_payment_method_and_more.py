# Generated by Django 5.0.1 on 2024-02-17 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_churchexpense_sabbath'),
    ]

    operations = [
        migrations.AddField(
            model_name='titheoffering',
            name='payment_method',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Bank', 'Bank')], default='Cash', max_length=10),
        ),
        migrations.AddField(
            model_name='weeklytransaction',
            name='project_sum',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
