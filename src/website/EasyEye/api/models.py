from django.db import models

# Create your models here.


class SecondData(models.Model):

    start_time = models.DateTimeField()
    blink = models.PositiveSmallIntegerField(default=0)
    direction = models.PositiveSmallIntegerField(default=0)
    squint = models.PositiveSmallIntegerField(default=0)
    start_point = models.BooleanField(default=False)