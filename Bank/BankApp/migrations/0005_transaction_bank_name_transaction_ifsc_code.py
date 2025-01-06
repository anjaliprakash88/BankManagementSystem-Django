# Generated by Django 5.1.1 on 2024-10-15 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankApp', '0004_transaction_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='bank_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]