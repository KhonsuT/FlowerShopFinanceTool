# Generated by Django 5.1.3 on 2024-12-01 20:53

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("FlowerShopFinanceTool", "0007_alter_flower_image_alter_prices_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flower",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="flower",
            name="image",
            field=models.ImageField(
                default="uploads/no_image.jpg", upload_to="uploads/"
            ),
        ),
        migrations.AlterField(
            model_name="prices",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 12, 1, 20, 53, 18, 533782, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="prices",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid3, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
