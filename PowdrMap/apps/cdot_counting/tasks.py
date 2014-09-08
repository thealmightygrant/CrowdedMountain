#!/usr/bin/env python
from celery import task
from .xml_count import cdotXMLReader
from .xml_parse import cdotXMLParser
from .models import HighwaySegment

#each task must start with @app.task
#the ignore_result is if we don't want the state to be stored
#@task(ignore_result=True) 
#def print_hello():
#    print 'hello there'


#@task()
#def gen_prime(x):
#    multiples = []
#    results = []
#    for i in xrange(2, x + 1):
#        if i not in multiples:
#            results.append(i)
#            for j in xrange(i*i, x+1, i):
#                multiples.append(j)
#    return results

#TODO: separate this so that we don't have to login every time (if possible)
#NOTE: by agreement with CDOT, don't reference more than once every 2 minutes
@task()
def gen_speed_values():
    reader = cdotXMLReader()
    data = reader.open_cdot_feed(cdot_url = 'https://data.cotrip.org/xml/speed_segments.xml')
    parser = cdotXMLParser(data)
    parser.prune_data()
    parser.store_highway_data()

#@task()
#def aggregate_hourly_data():
#    cdm.HighwaySegment.older_objects.aggregate_old_segments()
    
