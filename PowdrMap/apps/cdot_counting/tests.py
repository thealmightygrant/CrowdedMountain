"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError

from .xml_count import cdotXMLReader
from .xml_parse import cdotXMLParser
from .models import HighwaySegment
import re
import datetime
import random

#import optical_flow_count
#from django.conf import settings
#import glob
#import os
#import sys
#import pdb

'''class OpticalFlowTests(TestCase):
    def setUp(self):
        self.load_car_videos()

    def load_car_videos(self):
        media_loc = settings.MEDIA_ROOT
        self.video_files = glob.glob(media_loc + "*.flv")
        self.car_count_files = glob.glob(media_loc + "car_count*.txt")

    def test_loading_car_files(self):
        pass'''

class AggregateTestCase(TestCase):
    #TODO: perhaps have this call another class that creates test HighwaySegments

    def setUp(self):

        self.mile_marker_list = [177.0, 189.4, 195.4, 200.7, 205.5, 211.0, 213.6, 216.3, 221.3, 227.9, 232.3, 232.7, 239.7]
        #must be 1 or more to perform correctly
        #tests with data back X number of days beyond the last 24 hours
        self.days = 1

        for i in range(1000):
            self.create_fake_segment()

    def create_fake_segment(self):
        
        h = HighwaySegment()
        h.highway_name = 'I-70'
        #NOTE: There is sometimes a 0.1 mile difference in start markers for EAST and WEST 
        #        FOR EXAMPLE: 221.2 E and 221.3 W, doublecheck 232.3 and 232.7
        #        Names are a better unique identifier
        h.start_mile_marker = self.mile_marker_list[random.randrange(len(self.mile_marker_list) - 1)]  
        h.end_mile_marker = self.mile_marker_list[self.mile_marker_list.index(h.start_mile_marker) + 1];
        h.direction = 'E'
        #TODO: Perhaps, make this a parameter, right now 5% of the dates are within 1 day
        if random.random() < 0.95:
            h.datetime_calculated = self.random_date(datetime.datetime.now() - datetime.timedelta(days=(1 + self.days)), datetime.datetime.now() - datetime.timedelta(days=1))
        else:
            h.datetime_calculated = self.random_date(datetime.datetime.now() - datetime.timedelta(days=1), datetime.datetime.now())
        h.current_travel_time = random.randrange(35)
        h.expected_travel_time = random.randrange(25)
        h.avg_volume = random.randrange(5) + 1
        h.avg_occupancy = random.randrange(10) + 1
        #print h
        h.save()

    def random_date(self, start, end):
        delta = end - start
        #NOTE: only days, seconds, and microseconds are stored internally for timedelta objects
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + datetime.timedelta(seconds=random_second)

    def test_old_segment_manager(self):
        old_segs_qs = HighwaySegment.older_objects.all()
        for seg in old_segs_qs:
            self.assertGreaterEqual((datetime.datetime.now() - seg.datetime_calculated), datetime.timedelta(days=1))

    def test_aggregate_old_segments(self):
        HighwaySegment.older_objects.aggregate_old_segments()
        old_segs_qs = HighwaySegment.older_objects.all()
        
        #assuming 1 day here (i.e. 24 hours), must be modified if otherwise
        #Should be less than the number of possible segments, times the number of hours
        self.assertLessEqual(len(old_segs_qs), (len(self.mile_marker_list) - 1) * self.days * 24)


class XMLReaderTestCase(TestCase):

    def setUp(self):
        self.reader = cdotXMLReader()

    def test_cdot_feed_is_acquired(self):
        data = self.reader.open_cdot_feed(cdot_url = 'https://data.cotrip.org/xml/speed_segments.xml')
        self.assertIsNot(data, None)

class XMLParserTestCase(TestCase):

    def setUp(self):
        self.reader = cdotXMLReader()
        data = self.reader.open_cdot_feed(cdot_url = 'https://data.cotrip.org/xml/speed_segments.xml')
        self.parser = cdotXMLParser(data)
        self.parser.prune_data()

    def test_workspace_pruned(self):
        for node in self.parser.root.iter():
            match = re.search(r'({http://[\w./]+})(\w+)', node.tag)
            self.assertIs(match, None)

    def test_nothing_outside_i70(self):
        for node in self.parser.root.findall('Segment'):
            self.assertEqual(node.find('RoadName').text, r'I-70')

    def test_start_end_mm(self):
        for node in self.parser.root.findall('Segment'):
            start = float(node.find('StartMileMarker').text)
            end = float(node.find('EndMileMarker').text)
            self.assertGreater(end, start)
            self.assertGreaterEqual(start, 177.0)
            self.assertLessEqual(end, 239.7)

    def test_validation_segments(self):
        h = HighwaySegment()
        h.highway_name = 'I-70'
        h.start_mile_marker = 177.0
        h.end_mile_marker = 184.0
        h.direction = 'SE'
        h.datetime_calculated = datetime.datetime.now()
        h.current_travel_time = 10
        h.expected_travel_time = 20
        h.avg_volume = -1
        h.avg_occupancy = 5
        with self.assertRaises(ValidationError):
            h.full_clean()
        h.avg_occupancy = -1
        with self.assertRaises(ValidationError):
            h.full_clean()
        h.avg_volume = 5
        with self.assertRaises(ValidationError):
            h.full_clean()
        h.avg_occupancy = 5


if __name__ == "__main__":
    unittest.main()
