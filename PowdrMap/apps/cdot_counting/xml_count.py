#!/usr/bin/env python
from xml.etree import cElementTree       #C implementation of xml.etree.ElementTree
from xml.parsers.expat import ExpatError #XML formatting errors
from parse_xml import cdotXMLParser
import urllib2


# catch url not opening error and xml formatting errors

class cdotXMLReader:

    def __init__(self, cdot_url = 'https://data.cotrip.org/xml/speed_segments.xml'):
        #TODO: move this and any other SECRETS to something more secure,
        #       NOTE that this cannot work with a relative file location!
        f = open('/home/sherrick/external_projects/PowdrMap/PowdrMap/apps/cdot_counting/cdot_info', 'r')
        username = f.readline().rstrip()
        password = f.readline().rstrip()
        pagehandle = self.open_cdot_feed(cdot_url, username, password)
        if pagehandle is not None:
            self.data = pagehandle.read()


    def open_cdot_feed(self, cdot_url, user_name, password):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, cdot_url, user_name, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        try:
            cdot_xml = urllib2.urlopen(cdot_url)
            return cdot_xml
        except urllib2.HTTPError, err:
            if err.code == 401:
                print "Authorization failure to CDOT"
            if err.code == 404:
                print "Page not found, CDOT pages may be down"
            else:
                print "Error opening CDOT page: ", err.code
        except urllib2.URLError, err:
            print "Error opening CDOT page: ", err.code



if __name__ == "__main__":
    reader = cdotXMLReader(cdot_url = 'https://data.cotrip.org/xml/speed_segments.xml')
    parser = cdotXMLParser(reader.data)
    parser.prune_data()
    parser.print_xml()
