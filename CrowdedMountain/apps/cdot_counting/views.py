from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
#from CrowdedMountain.apps.cdot_counting.models import Resort
import datetime

#each view takes at least one parameter called a request
#  The request contains information about the current
#     web request that has triggered the view
#  It is an instance of the class django.http.HttpRequest
#  A view is just a Python function that takes an HttpRequest
#    as its first paramter and returns an instance of an HttpResponse

def ugly_count(request):
    abasin = 0
    loveland = 0
    keystone = 0
    breck = 0
    beaver_creek = 0
    vail = 0
    t = get_template('cdot_template.html')
    html = t.render(Context({'breck': breck,
                             'abasin': abasin,
                             'loveland': loveland,
                             'keystone': keystone,
                             'beaver_creek': beaver_creek,
                             'vail': vail}))
    return HttpResponse(html)

