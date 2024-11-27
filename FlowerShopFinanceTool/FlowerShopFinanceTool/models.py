from django.db import models

# models
## db
## flower - prices - type - id
##


class Flower(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class Prices(models.Model):
    name = models.ForeignKey(Flower, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "date"

    def __str__(self) -> str:
        return self.name
