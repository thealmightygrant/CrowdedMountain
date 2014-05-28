#!/usr/bin/env python
from django.db import models

class Location(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)

    def __unicode__(self):
        return self.address


     #other possible locations: GIS location(lat, long), Local location (within the resort, where is it)
     # Lifts and lift locations will be done in a different django app


#collected every two minutes from cdot
class HighwaySegment(models.Model):
    highway_name = models.CharField(max_length=20)
    start_mile_marker = models.DecimalField(max_digits=8, decimal_places=2)
    end_mile_marker = models.DecimalField(max_digits=8, decimal_places=2)
    direction = models.CharField(max_length=10)
    datetime_calculated = models.DateTimeField()
    current_travel_time = models.IntegerField()  #in minutes
    expected_travel_time = models.IntegerField() #in minutes

    #NOTE: avg volume and occupancy sometimes come in as -1, which means no reading
    avg_volume = models.IntegerField(blank=True, null=True) # in number of cars
    avg_occupancy = models.IntegerField(blank=True, null=True) # in percentage over last 2 minutes

    class Meta:
        ordering = ['highway_name','datetime_calculated']


class Resort(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location)
    add_segments = models.ManyToManyField(HighwaySegment, related_name='add_segments')
    sub_segments = models.ManyToManyField(HighwaySegment, related_name='sub_segments')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class CountStatistic(models.Model):
    count = models.IntegerField()
    date = models.DateTimeField()
    resort = models.ForeignKey(Resort)

    class Meta:
        ordering = ['resort','date']

    def __unicode__(self):
        return u'%s %s' % (self.resort.name, self.count)
