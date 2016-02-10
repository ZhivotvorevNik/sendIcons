from django.db import models

# Create your models here.
class Zone(models.Model):
    name = models.CharField(max_length=200)
    zone_id = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    service_id = models.CharField(max_length=200)
    zones = models.ManyToManyField(Zone, related_name="services")

    def __str__(self):
        return self.name
