from django.db import models

class Location(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)

    def __unicode__(self):
        return self.address

class Resort(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return self.name

class CountStatistic(models.Model):
    count = models.IntegerField()
    date = models.DateTimeField()
    resort = models.ForeignKey(Resort)

    class Meta:
        ordering = ['resort','date']

    def __unicode__(self):
        return u'%s %s' % (self.resort.name, self.count)
