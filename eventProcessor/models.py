from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser


class SessionID(models.Model):
    sessionID = models.UUIDField(primary_key=True)
    client = models.ForeignKey('Client', name='cookie', on_delete=models.RESTRICT)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()


class Client(models.Model):
    user = models.CharField(primary_key=True, max_length=32)
    password = models.CharField(max_length=32)


class PostalCode(models.Model):
    postal_code = models.IntegerField(primary_key=True)


class Installation(models.Model):
    installation = models.IntegerField(primary_key=True)
    device = models.IntegerField()
    postal_code = models.ForeignKey('PostalCode', on_delete=models.RESTRICT, name='installations')
    direction = models.CharField(max_length=200)
    UniqueConstraint(fields=['installation', 'device'], name='unique_device')


class NotableIncidents(models.Model):
    installation = models.ForeignKey('Installation', on_delete=models.RESTRICT, name='notable_incidents')
    timestamp = models.IntegerField()
    type = models.CharField(max_length=30)
    UniqueConstraint(fields=['installation', 'timestamp'], name="unique_notable_incidents")

    def serialize(self):
        return {
            "installation": self.installation,
            "timestamp": self.timestamp,
            "type": self.type
        }


class ExternalIncidents(models.Model):
    postal_code = models.ForeignKey('PostalCode', on_delete=models.RESTRICT, name='external_incidents', primary_key=True)
    timestamp = models.IntegerField()
    type = models.CharField(max_length=30)
    UniqueConstraint(fields=['postal_code', 'timestamp'], name="unique_external_incidents")

    def serialize(self):
        return {
            "installation": self.postal_code,
            "timestamp": self.timestamp,
            "type": self.type
        }


class Sensor(models.Model):
    id = models.IntegerField(primary_key=True)
    installation = models.IntegerField()
    postal_code = models.ForeignKey('PostalCode', on_delete=models.RESTRICT, name='sensors')
    direction = models.CharField(max_length=200, default=None)
    UniqueConstraint(fields=['id', 'installation'], name='unique_sensor')


class Example(models.Model):
    pass