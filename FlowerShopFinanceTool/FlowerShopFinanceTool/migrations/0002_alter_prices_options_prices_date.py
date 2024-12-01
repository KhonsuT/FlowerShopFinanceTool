# Generated by Django 5.1.3 on 2024-11-29 17:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("FlowerShopFinanceTool", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="prices",
            options={"get_latest_by": "date"},
        ),
        migrations.AddField(
            model_name="prices",
            name="date",
            field=models.DateField(
                default=datetime.datetime(2024, 11, 29, 17, 8, 57, 832079)
            ),
        ),
    ]
