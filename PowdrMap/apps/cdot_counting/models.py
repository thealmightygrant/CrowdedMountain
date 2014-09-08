#!/usr/bin/env python
from django.db import models
from django.db.models import Avg
from django.core.exceptions import ValidationError
import datetime

# A model manager that takes care of grabbing any HighwaySegment data that 
# was not in the last 24 hours
class OldHighwaySegmentManager(models.Manager):
    def get_query_set(self):
        #filter out every HW segment from the db from the last 24 hours
        return super(OldHighwaySegmentManager, self).get_query_set().filter(datetime_calculated__lt=(datetime.datetime.now() - datetime.timedelta(days=1))).order_by('datetime_calculated')

    def aggregate_old_segments(self):
        older_segs = self.get_query_set()
   
        count = 0
        #TODO: separate this out into more managable chunks, if possible
        if older_segs.exists():
            min_dt = older_segs[0].datetime_calculated
            min_dt.replace(minute = 0, second = 0, microsecond = 0)
            print min_dt

        while older_segs.exists():
            #get all of the segments that are within an hour
            one_hour_segs = older_segs.filter(datetime_calculated__range=(min_dt, min_dt + datetime.timedelta(hours=1)))
            #replace all of the others into the older_segs QuerySet
            older_segs = older_segs.exclude(datetime_calculated__range=(min_dt, min_dt + datetime.timedelta(hours=1)))

            count = count + 1
            min_dt = min_dt + datetime.timedelta(hours=1)        

            #print 'Number within hour ', count, ':', len(one_hour_segs)

            while one_hour_segs.exists():
                #aggregate all of the segments that are the same (i.e. start, end, and direction)
                same_segs = one_hour_segs.filter(
                    start_mile_marker__exact=(one_hour_segs[0].start_mile_marker),
                    end_mile_marker__exact=(one_hour_segs[0].end_mile_marker),
                    direction__iexact=(one_hour_segs[0].direction),
                    highway_name__iexact=(one_hour_segs[0].highway_name)
                    )
                 
                #remove it from the original QuerySet
                one_hour_segs = one_hour_segs.exclude(
                    start_mile_marker__exact=(one_hour_segs[0].start_mile_marker),
                    end_mile_marker__exact=(one_hour_segs[0].end_mile_marker),
                    direction__iexact=(one_hour_segs[0].direction),
                    highway_name__iexact=(one_hour_segs[0].highway_name)
                    )
                
                #print 'Number with same markers: ', len(same_segs)

                #TODO: will same_segs always exists?
                h = HighwaySegment(highway_name = same_segs[0].highway_name[:],
                                   #slice used here to perform deep copies of the strings
                                   direction = same_segs[0].direction[:], 
                                   datetime_calculated = same_segs[0].datetime_calculated,
                                   start_mile_marker = same_segs[0].start_mile_marker,
                                   end_mile_marker = same_segs[0].end_mile_marker,
                                   current_travel_time = int(same_segs.aggregate(Avg('current_travel_time'))['current_travel_time__avg']),
                                   expected_travel_time = int(same_segs.aggregate(Avg('expected_travel_time'))['expected_travel_time__avg']),
                                   avg_volume = int(same_segs.aggregate(Avg('avg_volume'))
                                                    ['avg_volume__avg']),
                                   avg_occupancy = int(same_segs.aggregate(Avg('avg_occupancy'))
                                                       ['avg_occupancy__avg'])
                                   )
                
                
                try:
                #Calls in this order:
                    #  clean_fields(): validate each field separately
                    #  clean(): see model for particulars, provides custom validation
                    #  validate_unique(): validates all unique constraints, 
                    #       requires setting unique_together constraint in model
                    h.full_clean()
                except ValidationError as e:
                    #TODO: check to see if continue is the right thing to do here
                    continue
                same_segs.delete()
                h.save()


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
        #don't allow for entries to have any negative numeric values
        #particularly, we are worried about avg_volume and avg_occupancy
        if self.avg_volume < 0 or self.avg_occupancy < 0:
            raise ValidationError('Highway Segments must have an avg volume and avg occupancy')

    def __unicode__(self):
        return u'%s %s %s' % (self.avg_occupancy, self.start_mile_marker, self.end_mile_marker)

    class Meta:
        ordering = ['highway_name','start_mile_marker']


class Location(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)

    def __unicode__(self):
        return self.address

    #other possible locations: GIS location(lat, long), #Local location (within the resort, where is it), Lifts and lift locations will be done in a different django app


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
    
    def __unicode__(self):
        return u'%s %s' % (self.resort.name, self.count)

    class Meta:
        ordering = ['resort','date']
