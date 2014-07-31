#!/usr/bin/env python
from django.db import models
import datetime

class Location(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)

    def __unicode__(self):
        return self.address


     #other possible locations: GIS location(lat, long), Local location (within the resort, where is it)
     # Lifts and lift locations will be done in a different django app


# A manager that takes care of grabbing any HighwaySegment data that was not in the last 24 hours
class OldHighwaySegmentManager(models.Manager):
    def get_query_set(self):
        return super(OldHighwaySegmentManager, self).get_query_set().filter(datetime_calculated__lt=(datetime.datetime.now() - datetime.timedelta(days=1)))

    def aggregate_old_segments(self):
        older_segs = self.get_query_set()
        
        while older_segs.exists():
            loop_dt = older_segs[0].datetime_calculated
            loop_dt.replace(minute = 0, second = 0, microsecond = 0)
            one_hour_segs = older_segs.filter(datetime_calculated__range=(loop_dt, loop_dt + datetime.timedelta(hours=1)))
            older_segs = older_segs.exclude(datetime_calculated__range=(loop_dt, loop_dt + datetime.timedelta(hours=1)))

            while one_hour_segs.exists():
                same_segs = one_hour_segs.filter(start_mile_marker__exact=(one_hour_segs[0].start_mile_marker)).filter(end_mile_marker__exact=(one_hour_segs[0].end_mile_marker), one_hour_segs[0].end_mile_marker).filter(direction__iexact=one_hour_segs[0].direction)
                
                #TODO: finish or replace the following statment that excludes all of the things from the previos statement
                one_hour_segs = one_hour_segs.exclude(highwayname__iexact=one_hour_segs[0].highway_name, direction__iexact=one_hour_segs[0].direction)
                
                #slice used here to perform deep copies of the strings
                h = HighwaySegment(highway_name = one_hour_segs[0].highway_name[:], start 
                same_segs.aggregate(Avg('avg_volume'))
            #TODO: make a second filter here to avg over things from the same segment, going the same direction

        
        #from django.db import connection
        #cursor = connection.cursor()
        #cursor.execute("""
        #""")
        


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

    objects = models.Manager()
    older_objects = OldHighwaySegmentManager()

    def clean(self):
        from django.core.exceptions import ValidationError
        #don't allow for entries to have any negative numeric values
        #particularly, we are worried about avg_volume and avg_occupancy
        if self.avg_volume < 0 or self.avg_occupancy < 0:
            raise ValidationError('Highway Segments must have an avg volume and avg occupancy')

    class Meta:
        ordering = ['highway_name','start_mile_marker']


class Resort(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class CountStatistic(models.Model):
    count = models.IntegerField()
    date = models.DateTimeField()
    approximation = models.BooleanField()
    resort = models.ForeignKey(Resort)

    class Meta:
        ordering = ['resort','date']

    def __unicode__(self):
        return u'%s %s' % (self.resort.name, self.count)
