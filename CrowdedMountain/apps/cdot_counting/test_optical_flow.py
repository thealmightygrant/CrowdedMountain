#!/usr/bin/env python
import optical_flow_count
import glob
import os
from django.conf import settings
from django.test import TestCase

class FirstTest(TestCase):
    #remember to name them test_something 
    # or they won't be found by unittest
    def setUp(self):
        self.load_car_videos()

    def load_car_videos(self):
        media_loc = settings.MEDIA_ROOT
        test_files = glob.glob(media_loc + "*.flv")
        car_count_files = glob.glob(media_loc + "car_count*.txt")
        print test_files
        print car_count_files
            
    def test_dummy1(self):
        pass
    def test_dummy2(self):
        pass

if __name__ == '__main__':
    #run all tests
    unittest.main()
