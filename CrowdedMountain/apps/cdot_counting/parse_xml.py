#!/usr/bin/env python
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class cdotXMLParser:

    def __init__(self, data=None):
        self.data = data
        self.root = ET.fromstring(self.data)

        #remove '{http://www.cotrip.org/schema/speed}' from start of each tag
        for node in self.root.iter():
            node.tag = node.tag[36:]


    def prune_data(self):
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
                start, end = end, start
            if start < 177.0 or end > 239.7:
                self.root.remove(node)


    def print_xml(self):
        for node in self.root.iter():
            print node.tag, node.text
