from django.contrib import admin
from CrowdedMountain.apps.cdot_counting.models import Resort, CountStatistic, HighwaySegment, Location

admin.site.register(Resort)
admin.site.register(CountStatistic)
admin.site.register(Location)
admin.site.register(HighwaySegment)
