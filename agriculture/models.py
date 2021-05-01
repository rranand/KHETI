from django.contrib.gis.db import models as gis
from django.db import models


class fields(models.Model):
    name = models.CharField(max_length=256)
    location = gis.PolygonField()

    obj = models.Manager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class weed_image(models.Model):
    img = models.ImageField(upload_to="images/")

    def __str__(self):
        return str(self.img)
