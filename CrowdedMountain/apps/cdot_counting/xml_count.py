#!/usr/bin/env python
from xml.etree import cElementTree       #C implementation of xml.etree.ElementTree
from xml.parsers.expat import ExpatError #XML formatting errors
import urllib

# catch url not opening error and xml formatting errors

def parse_xml(xml_url):
    f = urllib.urlopen(xml_url)
    tree = cElementTree.parse(f)
    for node in tree.getiterator():
        print node.tag, node.attrib





if __name__ == "__main__":
    parse_xml('http://www.coloradodot.info/tocFeeds/RSS1_SPD.xml')
