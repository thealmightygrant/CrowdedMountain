#!/usr/bin/env python
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import re
from models import HighwaySegment
from dateutil import parser as dtp

from django.core.exceptions import ValidationError

class cdotXMLParser:

    def __init__(self, data=None):
        self.data = data
        self.root = ET.fromstring(self.data)

    def prune_data(self, setup_for_resorts = True):
        #remove workspace, '{http://www.cotrip.org/schema/speed}' from start of each tag
        for node in self.root.iter():
            match = re.search(r'({http://[\w./]+})(\w+)', node.tag)
            node.tag = match.group(2)

        if setup_for_resorts:
        #remove everything that's not on I-70
            for node in self.root.findall('Segment'):
                for child in node.iter('RoadName'):
                    if child.text != 'I-70':
                        self.root.remove(node)

        #remove anything not close to the ski areas
        #MM 177.0 (East Vail) to 239.7 (Idaho Springs)
        for node in self.root.findall('Segment'):
            start = float(node.find('StartMileMarker').text)
            end = float(node.find('EndMileMarker').text)
            if start > end:
                node.find('StartMileMarker').text, node.find('EndMileMarker').text = \
                    node.find('EndMileMarker').text, node.find('StartMileMarker').text
                start, end = end, start
            if start < 177.0 or end > 239.7:
                self.root.remove(node)


    def store_highway_data(self):
        #TODO: store each segment for now, but eventually this should be thrown out
        for node in self.root.findall('Segment'):
            h = HighwaySegment()
            h.highway_name = node.find('RoadName').text
            h.start_mile_marker = float(node.find('StartMileMarker').text)  
            h.end_mile_marker = float(node.find('EndMileMarker').text)
            h.direction = node.find('Direction').text          
            h.datetime_calculated = dtp.parse(node.find('CalculatedDate').text)
            
            #TODO: should we be setting the value to None when there is an error to ensure it is caught??
            try:
                hours = node.find('TravelTime').find('Hours')
                minutes = node.find('TravelTime').find('Minutes')
                if hours is not None:
                    h.current_travel_time = (int(hours.text) * 60) + int(minutes.text)   # in minutes
                else:
                    h.current_travel_time = int(minutes.text)
            except ValueError as e:
                h.current_travel_time = 0
            except AttributeError as e:
                #when this happens, there is typically shit data
                #it means that there is no TravelTime element
                h.current_travel_time = 0

            try:
                hours = node.find('ExpectedTravelTime').find('Hours')
                minutes = node.find('ExpectedTravelTime').find('Minutes')
                if hours is not None:
                    h.expected_travel_time = (int(hours.text) * 60) + int(minutes.text)   # in minutes
                else:
                    h.expected_travel_time = int(minutes.text)
            except ValueError as e:
                h.expected_travel_time = 0
            except AttributeError as e:
                #when this happens, there is typically shit data
                #it means that there is no ExpectedTravelTime element
                h.expected_travel_time = 0

            h.avg_volume = int(node.find('AverageVolume').text)    # in # cars
            h.avg_occupancy = int(node.find('AverageOccupancy').text)   # in % over last 2 minutes
            try:
                h.full_clean()
            except ValidationError as e:
                continue
            h.save()

    def split_by_resort(self):
        #Find the resorts between each mile marker and store data
        pass

    def print_xml(self):
        for node in self.root.iter():
            print node.tag, node.text
