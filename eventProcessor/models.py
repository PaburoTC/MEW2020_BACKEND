from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser


class SessionID(models.Model):
    sessionID = models.UUIDField(primary_key=True)
    client = models.ForeignKey('Client', name='cookie', on_delete=models.RESTRICT)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()


class Client(models.Model):
    user = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    UniqueConstraint(fields=['user'], name='unique_sensor')


class Installation(models.Model):
    installation = models.IntegerField()
    postalCode = models.IntegerField()
    direction = models.CharField(max_length=200)


class NotableIncidents(models.Model):
    installation = models.ForeignKey('Installation', on_delete=models.RESTRICT, name='sensor')
    type = models.CharField(max_length=30)


class ExternalIncidents(models.Model):
    installation = models.ForeignKey('Installation', on_delete=models.RESTRICT, name='sensor')
    type = models.CharField(max_length=30)


class Sensor(models.Model):
    id = models.IntegerField(primary_key=True)
    installation = models.ForeignKey('Installation', on_delete=models.RESTRICT, name='sensor')
    UniqueConstraint(fields=['id', 'installation'], name='unique_sensor')
