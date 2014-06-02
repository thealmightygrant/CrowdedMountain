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
