from django.db import models


class VIN(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=200)
    year = models.IntegerField(null=True)
    make = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=50, null=True)
    weight = models.JSONField(default=dict)
    dimensions = models.JSONField(default=dict)


# class Weight(models.Model):
#     """
#     Change UNITS constant as you want.
#     """
#     UNITS = [
#         ("KG", "Kilograms"),
#         ("LBS", "LBS"),
#     ]
#     type = models.CharField(max_length=100, null=True)
#     unit = models.CharField(max_length=5, choices=UNITS)
#     value = models.IntegerField(default=0)
#     vin = models.OneToOneField("vin.VIN", on_delete=models.CASCADE, related_name="weight")
