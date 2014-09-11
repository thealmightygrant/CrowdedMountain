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

if __name__ == "__main__":
    unittest.main()
