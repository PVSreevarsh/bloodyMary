# Generated by Django 4.1.7 on 2024-05-12 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0003_sme_phonenumber_alter_sme_amtpaid_alter_sme_askamt_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sector",
            old_name="sector_performance",
            new_name="risk_classification",
        ),
    ]