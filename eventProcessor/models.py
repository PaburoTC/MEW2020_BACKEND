from django.db import models
from django.db.models import UniqueConstraint

class Sensor(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="sensors")
    instalation = models.IntegerField()
    UniqueConstraint(fields=['id','instalation'], name='unique_sensor')