# Generated by Django 5.1.3 on 2024-11-29 20:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("FlowerShopFinanceTool", "0004_alter_prices_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="flower",
            name="image",
            field=models.ImageField(
                default="static/uploads/no_image.jpg", upload_to="static/uploads/"
            ),
        ),
        migrations.AlterField(
            model_name="prices",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 11, 29, 20, 2, 41, 341039, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
