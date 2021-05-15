from django.contrib.gis.db import models as gis
from django.db import models


class image_model(models.Model):
    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to="images/")

    def __str__(self):
        return str(self.img)

    def __unicode__(self):
        return str(self.img)


class location_model(models.Model):
    name = gis.CharField(max_length=250)
    location = gis.MultiPolygonField()

    objects = models.Manager()

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

