#!/usr/bin/env python
from xml.etree import cElementTree       #C implementation of xml.etree.ElementTree
from xml.parsers.expat import ExpatError #XML formatting errors

import urllib2

class cdotXMLReader:

    def __init__(self):
        #TODO: move this and any other SECRETS to something more secure,
        #TODO: this does not work with a relative file location at the moment!
        f = open('/home/sherrick/external_projects/PowdrMap/PowdrMap/apps/cdot_data_collector/cdot_info', 'r')
        self.username = f.readline().rstrip()
        self.password = f.readline().rstrip()

    def open_cdot_feed(self, cdot_url=None):
        '''Open CDOT XML Feeds, returns XML data, see schemas at: http://www.cotrip.org/xmlFeed.htm '''
        xml_data = None


        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, cdot_url, self.username, self.password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        # catch url not opening error and xml formatting errors
        try:
            cdot_xml = urllib2.urlopen(cdot_url)
            xml_data = cdot_xml.read()
        except urllib2.HTTPError, err:
            if err.code == 401:
                print "Authorization failure to CDOT"
            if err.code == 404:
                print "Page not found, CDOT pages may be down"
            else:
                print "Error opening CDOT page: ", err.code
        except urllib2.URLError, err:
            print "Error opening CDOT page: ", err.args
        except IOError:
            print "Error reading CDOT page"
        
        return xml_data

if __name__ == "__main__":
    reader = cdotXMLReader()
    data = reader.open_cdot_feed(cdot_url = 'https://data.cotrip.org/xml/speed_segments.xml')
