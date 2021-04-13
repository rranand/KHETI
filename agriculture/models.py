from django.db import models


class weed_image(models.Model):
    img = models.ImageField(upload_to="images/")

    def __str__(self):
        return str(self.img)
