from django.http import HttpResponse

from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect

#each view takes at least one parameter called a request
#  The request contains information about the current
#     web request that has triggered the view
#  It is an instance of the class django.http.HttpRequest
#  A view is just a Python function that takes an HttpRequest
#    as its first paramter and returns an instance of an HttpResponse

def home(request):
    t = get_template('home.html')
    html = t.render(Context({}))
    return HttpResponse(html)
