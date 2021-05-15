import random
import string
import json
import requests

from django.contrib.gis.geos import Polygon, MultiPolygon
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from Disease.frontenddisease import plant_disease_predict
from ndvi_plot import plot
from weed_checker import predict, soil_fertilizer_predict, crop_recommendations_predict
from .form import upload_img_set, soil_fertilizer_form, crop_recommendations_form, upload_img_only, upload_two_image
from .models import image_model, location_model


def getWeatherData(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid=4015ab7e293195754dcb1941243c605a'

    js = json.loads(requests.get(url.format(str(request.ipinfo.latitude), str(request.ipinfo.longitude))).text)
    return js


def home(request):
    return render(request, "home.html")


def weed_r(request):
    f1 = upload_img_set()

    if request.method == 'POST':
        f1 = upload_img_set(request.POST, request.FILES)

        obj = []
        letters = string.ascii_lowercase
        nm = (''.join(random.choice(letters) for i in range(10)))
        letters = string.ascii_uppercase
        nm += (''.join(random.choice(letters) for i in range(10)))
        letters = string.ascii_letters
        nm += (''.join(random.choice(letters) for i in range(10)))
        letters = string.digits
        nm += (''.join(random.choice(letters) for i in range(10)))

        for ff in f1:
            if ff.is_valid():
                try:
                    img = ff.cleaned_data['image']
                    ord = str(ff.cleaned_data['ordinates']).split(' ')
                except KeyError:
                    continue

                ord_f = []
                for i in ord:
                    ord_f.append(tuple(map(float, i.split('#'))))

                f = image_model.objects.create(name=nm, img=img)
                f.save()

                flag = predict(str(f.img))
                if flag:
                    obj.append(Polygon(tuple(ord_f)))

        if len(obj) == 0:
            return render(request, 'weed.html', context={'form': f1, 'present': 'b'})
        else:
            loc = location_model.objects.create(name=nm, location=MultiPolygon(tuple(obj)))
            loc.save()
            return render(request, 'weed.html', context={'form': f1, 'loc': loc.name, 'present': 'a'})

    return render(request, 'weed.html', context={'form': f1})


def get_location(request):
    response_data = {'data': None}
    location = get_object_or_404(location_model, name=request.GET['name'])

    response_data['data'] = {
        'polygons': location.location.geojson,
        'title': location.name
    }

    return JsonResponse(response_data)


def soil_fertilizer(request):
    data = getWeatherData(request)
    weData = {'temp': str(data['main']['temp']), 'humidity': str(data['main']['humidity']), 'moisture': str(14)}

    f1 = soil_fertilizer_form(initial=weData)

    if request.method == 'POST':
        f1 = soil_fertilizer_form(request.POST)

        if f1.is_valid():
            t = float(f1.cleaned_data['temp'])
            h = float(f1.cleaned_data['humidity'])
            m = float(f1.cleaned_data['moisture'])
            s = f1.cleaned_data['soil']
            c = f1.cleaned_data['crop']
            n = float(f1.cleaned_data['nitrogen'])
            k = float(f1.cleaned_data['potassium'])
            p = float(f1.cleaned_data['phosphorus'])

            x = soil_fertilizer_predict(t, h, m, s, c, n, k, p)

            return render(request, 'soil_fertilizer.html', {'f1': f1, 'predict': x})

    return render(request, 'soil_fertilizer.html', {'f1': f1})


def crop_recommend(request):
    data = getWeatherData(request)
    weData = {'temp': str(data['main']['temp']), 'humidity': str(data['main']['humidity']), 'rainfall': str(14)}

    f1 = crop_recommendations_form(initial=weData)

    if request.method == 'POST':
        f1 = crop_recommendations_form(request.POST)

        if f1.is_valid():
            n = float(f1.cleaned_data['nitrogen'])
            k = float(f1.cleaned_data['potassium'])
            p = float(f1.cleaned_data['phosphorus'])
            t = float(f1.cleaned_data['temp'])
            h = float(f1.cleaned_data['humidity'])
            ph = float(f1.cleaned_data['ph'])
            rainfall = float(f1.cleaned_data['rainfall'])

            x = crop_recommendations_predict(n, k, p, t, h, ph, rainfall)

            return render(request, 'crop_recommendation.html', {'f1': f1, 'predict': x})

    return render(request, 'crop_recommendation.html', {'f1': f1})


def plant_disease(request):
    f1 = upload_img_only()

    if request.method == 'POST':
        f1 = upload_img_only(request.POST, request.FILES)

        if f1.is_valid():
            img = f1.cleaned_data['image']

            f = image_model.objects.create(name=str(img), img=img)
            f.save()

            y = plant_disease_predict(str(f.img))
            x = y[0].split('___')[1].replace('_', ' ')

            context = {'f1': f1, 'predict': x, 'flag': 'healthy' == x}

            if len(y[1]) != 0:
                context['remedy'] = y[1]

            return render(request, 'plant_disease.html', context=context)

    return render(request, 'plant_disease.html', context={'f1': f1})


def irrigation_check(request):
    f1 = upload_two_image()

    if request.method == 'POST':
        f1 = upload_two_image(request.POST, request.FILES)

        if f1.is_valid():
            img_1 = f1.cleaned_data['img_1']
            img_2 = f1.cleaned_data['img_2']

            f = image_model.objects.create(name=str(img_1), img=img_1)
            f.save()

            g = image_model.objects.create(name=str(img_2), img=img_2)
            g.save()

            x = plot(f.img, g.img)
            if len(x) == 0:
                return render(request, "irrigation.html", context={'f1': f1, 'out': 1})
            else:
                return render(request, "irrigation.html", context={'f1': f1, 'data': x})
    return render(request, "irrigation.html", context={'f1': f1})
