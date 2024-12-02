from django.db import models
from django.utils import timezone
from .settings import MEDIA_ROOT
import uuid
# models
## db
## flower - prices - type - id
##


class Flower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    image = models.ImageField(
        upload_to="uploads/",
        default="uploads/no_image.jpg",
    )

    def __str__(self) -> str:
        return self.name


class Prices(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.ForeignKey(Flower, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now())

    class Meta:
        get_latest_by = "date"

    def __str__(self) -> str:
        return f"{self.name.name} - ${self.price:.2f}"
