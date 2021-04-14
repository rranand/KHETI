from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.gis.admin import OSMGeoAdmin


@admin.register(fields)
class FieldsAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')


admin.site.register(weed_image)
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = 'K.H.E.T.I.'
admin.site.site_title = 'K.H.E.T.I.\'s Admin Panel'
admin.site.index_title = 'Welcome to K.H.E.T.I.'
