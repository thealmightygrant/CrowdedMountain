#!/usr/bin/env python
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class cdotXMLParser:

    def __init__(self, data=None):
        self.data = data
    def print_xml(self):
        root = ET.fromstring(self.data)

        #remove '{http://www.cotrip.org/schema/speed}' from start of each tag
        for node in root.iter():
            node.tag = node.tag[36:]

        #remove everything that's not on I-70
        for node in root.findall('Segment'):
            for child in node.iter('RoadName'):
                if child.text != 'I-70':
                    #print child.text
                    root.remove(node)

        
        for node in root.iter():
            print node.tag, node.text
