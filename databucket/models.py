'''
Created on Oct 28, 2014

@author: lauril
'''
from django.db import models
from datetime import datetime

def convertDatetimeToString(o):
    DATE_FORMAT = "%Y-%m-%d" 
    TIME_FORMAT = "%H:%M:%S"

    if isinstance(o, datetime.date):
        return o.strftime(DATE_FORMAT)
    elif isinstance(o, datetime.time):
        return o.strftime(TIME_FORMAT)
    elif isinstance(o, datetime.datetime):
        return o.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
    


class Firestorm(models.Model):
    local_mac = models.CharField(primary_key=True ,max_length=30)
    name = models.CharField(max_length=30)
    description  = models.CharField(max_length=300)
    observations = models.IntegerField()
    seen = models.DateTimeField(auto_now=True)
    
    def save(self,*args, **kwargs):
        self.seen = datetime.now()
        super(Firestorm, self).save(*args, **kwargs)
        
    def __str__(self):
        return "FireStorm: %s last seen" %(self.local_mac, convertDatetimeToString(self.seen))

class FirestormReading(models.Model):
    observer = models.ForeignKey(Firestorm)
    recorded = models.DateTimeField(auto_now=True)
    acc_X = models.IntegerField( default=0,  null=True, blank=True)
    acc_Y = models.IntegerField( default=0,  null=True, blank=True)
    acc_Z = models.IntegerField( default=0,  null=True, blank=True)
    mag_X = models.IntegerField( default=0,  null=True, blank=True)
    mag_Y = models.IntegerField( default=0,  null=True, blank=True)
    mag_Z = models.IntegerField( default=0,  null=True, blank=True)
    light=models.IntegerField(default=0,  null=True, blank=True)
    
    def __str__(self):
        return "Sensory data reading for %s from %s" %(self.observer.local_mac, convertDatetimeToString(self.recorded))
           
class ObservedDevice(models.Model):
    observer = models.ForeignKey(Firestorm)
    local_mac = models.CharField(max_length=30)
    manufactorer  = models.CharField(max_length=30)
    seen = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return "Observed %s at %s" %(self.local_mac, convertDatetimeToString(self.seen))