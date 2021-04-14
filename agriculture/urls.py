from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('weed', views.weed_r, name='weed'),
    path('weedGeo', views.get_location, name='weedGeo'),

]
