'''
Created on Oct 28, 2014

@author: lauril
'''
from django.db import models
from datetime import datetime

def convertDatetimeToString(o):
    DATE_FORMAT = "%Y-%m-%d" 
    TIME_FORMAT = "%H:%M:%S"
    return o.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
    


class Firestorm(models.Model):
    local_mac = models.CharField(primary_key=True ,max_length=30)
    name = models.CharField(max_length=30)
    description  = models.CharField(max_length=300, null=True, blank=True)
    observations = models.IntegerField( default=0,  null=True, blank=True)
    data_points  = models.IntegerField( default=0,  null=True, blank=True)
    seen = models.DateTimeField(auto_now=True)
    
    
    def save(self,*args, **kwargs):
        self.seen = datetime.now()
        super(Firestorm, self).save(*args, **kwargs)

    def sensorReading(self):
        self.data_points+=1
        self.save()
        
    def seenDevice(self):
        self.observations+=1
        self.save()    
        
    def __str__(self):
        return "Firestorm %s last seen on %s" %(self.local_mac, str(self.seen.strftime("%Y-%m-%d %H:%M:%S")))
    
class FirestormReading(models.Model):
    firestorm = models.ForeignKey(Firestorm)
    recorded = models.DateTimeField(auto_now=True)
    acc_X = models.IntegerField( default=0,  null=True, blank=True)
    acc_Y = models.IntegerField( default=0,  null=True, blank=True)
    acc_Z = models.IntegerField( default=0,  null=True, blank=True)
    mag_X = models.IntegerField( default=0,  null=True, blank=True)
    mag_Y = models.IntegerField( default=0,  null=True, blank=True)
    mag_Z = models.IntegerField( default=0,  null=True, blank=True)
    light=models.IntegerField(default=0,  null=True, blank=True)

    def save(self,*args, **kwargs):
        self.firestorm.sensorReading()
        super(FirestormReading, self).save(*args, **kwargs)
        
    def __str__(self):
        return "data form %s recorded on %s" %(self.firestorm.local_mac, str(self.recorded.strftime("%Y-%m-%d %H:%M:%S")))    
    
class ObservedDevice(models.Model):
    observer = models.ForeignKey(Firestorm)
    observedMAC = models.CharField(max_length=30)
    manufactorer  = models.CharField(max_length=30)
    seen = models.DateTimeField(auto_now=True)
    
    def save(self,*args, **kwargs):
        self.observer.seenDevice()
        super(ObservedDevice, self).save(*args, **kwargs)
        
    def __str__(self):
        return "device %s observed on %s at %s" %(self.observedMAC, self.observer.local_mac , str(self.seen.strftime("%Y-%m-%d %H:%M:%S")))      

from django.contrib import admin       
admin.site.register(Firestorm)
admin.site.register(FirestormReading) 
admin.site.register(ObservedDevice)