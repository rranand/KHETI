from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('weed', views.weed_r, name='weed'),
    path('weedGeo', views.get_location, name='weedGeo'),
    path('soilFertilizer', views.soil_fertilizer, name='soilFertilizer'),
    path('cropRecommend', views.crop_recommend, name='cropRecommend'),
    path('plantDisease', views.plant_disease, name='plantDisease'),
]
