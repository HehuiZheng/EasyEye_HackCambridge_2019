from django.db import models

# Create your models here.


class SecondData(models.Model):

    start_time = models.DateTimeField()
    blink = models.PositiveSmallIntegerField(default=0)
    direction = models.FloatField(default=0)
    squint = models.FloatField(default=0)
    start_point = models.BooleanField(default=False)
    def __str__(self):
        return (str(self.start_time) + "||" + str(self.blink) + ' '
              + str(self.direction) + ' ' + str(self.squint) + ' ' + str(self.start_point))


class Alert(models.Model):

    start_time = models.DateTimeField()
    alert_wrong_direction = models.PositiveSmallIntegerField(default=0)
    alert_blink_slow = models.PositiveSmallIntegerField(default=0)
    alert_blur_sight = models.PositiveSmallIntegerField(default=0)
    alert_usage_overtime = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return 'Time: ' + str(self.start_time) + ' | ' + str(self.alert_wrong_direction) + str(self.alert_blink_slow) + str(self.alert_blur_sight)  + str(self.alert_usage_overtime)