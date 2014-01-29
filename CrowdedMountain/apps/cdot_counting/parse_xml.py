#!/usr/bin/env python
from xml.etree import cElementTree       #C implementation of xml.etree.ElementTree

class cdotXMLParser:

    def __init__(self, data=None):
        self.data = data

    def print_xml(self):
        tree = cElementTree.parse(self.data)
        for node in tree.getiterator():
            print node.tag, node.attrib, '\n'
