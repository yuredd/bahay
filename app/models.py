
from django.db import models

import datetime

# Create your models here.
class SystemSetting(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=150)
    def __str__(self):
        return "'{}' = '{}'".format(self.name, self.value)

class Job(models.Model):
    name = models.CharField(max_length=100)
    timetoexecute = models.DateTimeField()

class GPIOPin(models.Model):
    name = models.CharField(max_length=100)
    pin = models.IntegerField()

    MODE_CHOICES = (('BOARD', 'BOARD'), ('BCM','BCM'))
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='BCM')

    SETUP_CHOICES = (('IN', 'IN'), ('OUT','OUT'))
    setup = models.CharField(max_length=10, choices=SETUP_CHOICES, default='OUT')

    STATUS_CHOICES = (('HIGH', 'HIGH'), ('LOW','LOW'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='HIGH')

    def get_status(self):
        pass

    def set_high(self):
        pass

    def set_low(self):
        pass

    def __str__(self):
        return "{} ({}pin #{}): {}".format(self.name, self.mode, self.pin, self.status)

class Shutter(models.Model):
    name = models.CharField(max_length=100)
    faicon = models.CharField(max_length=100, default='bars', null=True, blank=True)
    gpiopinup = models.ForeignKey(GPIOPin, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    gpiopindown = models.ForeignKey(GPIOPin, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(default=0)

    timetoopen = models.IntegerField(null=True, blank=True, default=30)

    MODE_CHOICES = (('IDLE', 'IDLE'), ('GOINGUP','GOINGUP'), ('GOINGDOWN', 'GOINGDOWN'), ('MANUAL', 'MANUAL'))
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='IDLE')

    currentjob = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)

    def open(self):
        if self.mode == 'IDLE' and self.status < 100:
            self.mode = 'GOINGUP'
            secs = int(self.timetoopen * (100 / self.status))
            newjob = Job(name=self.name + '-' + self.mode, command=str(gpiopinup.pin) + '-0', timetoexecute=datetime.datetime.now() + datetime.timedelta(seconds=secs))
            newjob.save()
            self.currentjob = newjob

    def close(self):
        if self.mode == 'IDLE' and self.status > 0:
            self.mode = 'GOINGDOWN'
            secs = int(self.timetoopen * (100 / self.status))
            newjob = Job(name=self.name + '-' + self.mode, command=str(gpiopindown.pin) + '-1', timetoexecute=datetime.datetime.now() + datetime.timedelta(seconds=secs))
            newjob.save()
            self.currentjob = newjob

    def stop(self):
        pass

    def __str__(self):
        return "{} ({}): {}%".format(self.name, self.mode, self.status)
    


