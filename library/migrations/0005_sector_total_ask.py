# Generated by Django 4.1.7 on 2024-05-12 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0004_rename_sector_performance_sector_risk_classification"),
    ]

    operations = [
        migrations.AddField(
            model_name="sector",
            name="total_ask",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=12, null=True
            ),
        ),
    ]
